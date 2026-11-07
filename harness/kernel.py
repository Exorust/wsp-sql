"""Persistent Python kernel over the model weights (the editor's notebook).

Parent: Kernel(model_dir, work_dir).run(code) -> output text. Child process: exec code in one namespace; the prelude
defines NAMES, SHAPES, load, load_original, save_edit, drop_edit, edited, tok. Edits live in <work>/edited/<name>.npy
(float32). Restarted on timeout (variables lost; the caller is told).
ponytail: memory cap = RSS poll every 2 s (kill above 12 GB); isolation = sandbox-exec (deny network, deny writes outside work) + python -I + wall-clock limit.
"""
import json, os, subprocess, sys, time

TIMEOUT, MAX_OUT, MAX_GB = 900, 10_000, 12
FROZEN = ("model.language_model.norm.weight", "model.language_model.embed_tokens.weight", "lm_head.weight")

PRELUDE = r'''
import json, os, sys, io, contextlib, numpy as np, torch
torch.set_grad_enabled(False); torch.set_num_threads(8)
np.set_printoptions(precision=4, suppress=True, linewidth=160)
from safetensors import safe_open
from tokenizers import Tokenizer
MODEL, WORK, FROZEN = %r, %r, %r
_ST = safe_open(MODEL + "/model.safetensors-00001-of-00001.safetensors", "pt")
NAMES = sorted(_ST.keys())
SHAPES = {n: tuple(_ST.get_slice(n).get_shape()) for n in NAMES}
tok = Tokenizer.from_file(MODEL + "/tokenizer.json")
_ED = WORK + "/edited"
def _p(name): return f"{_ED}/{name}.npy"
def load_original(name):
    assert name in SHAPES, f"unknown tensor {name}"
    return _ST.get_tensor(name).float()
def load(name):
    return torch.from_numpy(np.load(_p(name))) if os.path.exists(_p(name)) else load_original(name)
def edited(): return sorted(f[:-4] for f in os.listdir(_ED)) if os.path.isdir(_ED) else []
def drop_edit(name):
    if os.path.exists(_p(name)): os.remove(_p(name)); return f"dropped edit of {name}"
    return f"no edit of {name}"
def save_edit(name, t):
    assert name in SHAPES, f"unknown tensor {name}"
    assert name not in FROZEN, f"refused: {name} is out of scope (final norm / embeddings / output layer)"
    t = torch.as_tensor(t).detach().float().cpu()
    assert tuple(t.shape) == SHAPES[name], f"shape {tuple(t.shape)} != {SHAPES[name]}"
    assert torch.isfinite(t).all(), "non-finite values"
    o = load_original(name); m = o.abs() > 1e-6
    if m.sum() > 0:
        r = (t[m] / o[m]); c = r.median()
        if (r - c).abs().max() < 1e-4 and abs(float(c) - 1.0) > 1e-6:
            raise AssertionError("refused: edit only multiplies the whole tensor by a constant")
    os.makedirs(_ED, exist_ok=True); np.save(_p(name), t.numpy())
    return f"saved edit of {name}: {int((t != o).sum())} of {t.numel()} entries changed, max |delta| {float((t-o).abs().max()):.4g}"
_NS = {}
def _run(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        try:
            import ast
            tree = ast.parse(code)
            if tree.body and isinstance(tree.body[-1], ast.Expr):
                last = ast.Expression(tree.body.pop().value)
                exec(compile(tree, "<cell>", "exec"), globals())
                v = eval(compile(last, "<cell>", "eval"), globals())
                if v is not None: print(repr(v))
            else:
                exec(compile(tree, "<cell>", "exec"), globals())
        except Exception:
            import traceback; traceback.print_exc()
    return buf.getvalue()
for _line in sys.stdin:
    _req = json.loads(_line)
    _out = _run(_req["code"])
    sys.__stdout__.write(json.dumps({"out": _out}) + "\n"); sys.__stdout__.flush()
'''


class Kernel:
    def __init__(self, model_dir, work_dir, python=sys.executable):
        self.model_dir, self.work_dir, self.python = os.path.abspath(model_dir), os.path.abspath(work_dir), python
        self.proc = None

    def start(self):
        os.makedirs(self.work_dir, exist_ok=True)
        code = PRELUDE % (self.model_dir, self.work_dir, FROZEN)
        # macOS sandbox: no network; writes only inside the work folder (plus temp/dev). Reads stay allowed (model, practice).
        home = os.path.expanduser("~"); proj = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pyroot = os.path.dirname(os.path.dirname(os.path.realpath(self.python)))  # uv-managed cpython lives under ~/.local
        profile = ('(version 1) (allow default) (deny network*) (deny file-write*) '
                   f'(allow file-write* (subpath "{self.work_dir}") (subpath "/private/tmp") (subpath "/private/var/folders") (subpath "/dev")) '
                   f'(deny file-read* (subpath "{home}")) (allow file-read-metadata (subpath "{home}")) (allow file-read* (subpath "{proj}") (subpath "{pyroot}"))')  # the agent reads only this project + its python
        self.proc = subprocess.Popen(["sandbox-exec", "-p", profile, self.python, "-I", "-u", "-c", code], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL, text=True, cwd=self.work_dir,
                                     env={"HOME": self.work_dir, "PATH": "/usr/bin:/bin", "OMP_NUM_THREADS": "8"})

    def run(self, code):
        """-> (output, restarted)"""
        if self.proc is None or self.proc.poll() is not None:
            self.start()
        t0 = time.time()
        self.proc.stdin.write(json.dumps({"code": code}) + "\n"); self.proc.stdin.flush()
        import select
        r = []
        while not r and time.time() - t0 < TIMEOUT:
            r, _, _ = select.select([self.proc.stdout], [], [], 2)
            rss = int(subprocess.run(["ps", "-o", "rss=", "-p", str(self.proc.pid)], capture_output=True, text=True).stdout or 0) / 2**20
            if not r and rss > MAX_GB:
                self.proc.kill(); self.proc = None
                return f"[the kernel used more than {MAX_GB} GB of memory; it was restarted and its variables are lost]", True
        if not r:
            self.proc.kill(); self.proc = None
            return f"[timed out after {TIMEOUT} s; the kernel was restarted and its variables are lost]", True
        line = self.proc.stdout.readline()
        if not line:
            self.proc = None
            return "[the kernel died (memory?) and was restarted; its variables are lost]", True
        out = json.loads(line)["out"]
        if len(out) > MAX_OUT:
            out = out[:MAX_OUT] + f"\n[output cut at {MAX_OUT:,} characters]"
        return (out or "(no output)") + f"\n[{time.time() - t0:.1f} s]", False

    def close(self):
        if self.proc:
            self.proc.kill()


if __name__ == "__main__":  # self-check
    import tempfile
    k = Kernel(os.path.join(os.path.dirname(__file__), "..", "models", "Qwen3.5-0.8B"), tempfile.mkdtemp())
    out, _ = k.run("len(NAMES), NAMES[100], SHAPES['model.language_model.layers.15.mlp.down_proj.weight']")
    print(out); assert "down_proj" in out or "1024" in out
    out, _ = k.run("W=load('model.language_model.layers.15.mlp.down_proj.weight'); save_edit('model.language_model.layers.15.mlp.down_proj.weight', W*2)")
    print(out); assert "refused" in out
    out, _ = k.run("W2=W.clone(); W2[:, :64]*=0.5; print(save_edit('model.language_model.layers.15.mlp.down_proj.weight', W2)); edited()")
    print(out); assert "saved edit" in out
    out, _ = k.run("try:\n    save_edit('model.language_model.embed_tokens.weight', load('model.language_model.embed_tokens.weight'))\nexcept Exception as e: print('ERR', e)")
    print(out); assert "out of scope" in out
    out, _ = k.run("tok.encode('SELECT 1').ids[:5]"); print(out)
    MAX_GB = 1
    out, restarted = k.run("x = torch.ones(400_000_000); import time; time.sleep(6)"); print(out); assert restarted and "memory" in out
    k.close(); print("kernel self-check OK")
