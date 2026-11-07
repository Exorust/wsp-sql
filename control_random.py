"""Random-edit control: same tensors, same number of changed columns, same per-column change vectors as an agent's edit,
but the columns are moved to random positions. If the agent's edit works and these do not, the location mattered.

usage: python control_random.py --footprint runs/fable_think_p25_r1/work/edited_model --draws 5 --out runs/ctrl_random_r1
       then evaluate each  <out>/draw_<k>/edited_model  with eval_sql.py like Phase 0.
ponytail: columns only (both edits so far were column edits); add row permutation if an agent edits rows.
"""
import argparse, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, f"{ROOT}/harness")
from baseline_sft import ST


def deltas(base, edited):
    """-> {name: (base float32 array, delta float32 array)} for tensors that differ"""
    from safetensors import safe_open
    a, b = safe_open(f"{base}/{ST}", "pt"), safe_open(f"{edited}/{ST}", "pt")
    out = {}
    for n in a.keys():
        x, y = a.get_tensor(n).float().numpy(), b.get_tensor(n).float().numpy()
        if (x != y).any(): out[n] = (x, y - x)
    assert out, "footprint is empty"
    return out


def shuffle_columns(delta, rng):
    """move each changed column's delta to a random unchanged-or-changed column, same count"""
    cols = np.flatnonzero(np.abs(delta).sum(0))
    new = rng.choice(delta.shape[1], len(cols), replace=False)
    d = np.zeros_like(delta); d[:, new] = delta[:, cols]
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=f"{ROOT}/models/Qwen3.5-0.8B"); ap.add_argument("--footprint", required=True)
    ap.add_argument("--draws", type=int, default=5); ap.add_argument("--seed", type=int, default=0); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    from forward import Forward
    ds = deltas(a.model, a.footprint)
    for k in range(a.draws):
        rng = np.random.default_rng(a.seed * 1000 + k); w = f"{a.out}/draw_{k}"; os.makedirs(f"{w}/edited", exist_ok=True)
        for n, (x, d) in ds.items():
            np.save(f"{w}/edited/{n}.npy", x + shuffle_columns(d, rng))
        Forward(a.model, w, f"{ROOT}/practice/spider_train.jsonl").build_edited()
        print("draw", k, "->", f"{w}/edited_model", {n: int(np.abs(d).sum(0).astype(bool).sum()) for n, (x, d) in ds.items()}, "columns")


if __name__ == "__main__":
    if len(sys.argv) == 1:  # self-check
        rng = np.random.default_rng(0); d = np.zeros((4, 10), np.float32); d[:, [2, 7]] = rng.normal(size=(4, 2))
        s = shuffle_columns(d, rng)
        assert (np.abs(s).sum(0) > 0).sum() == 2 and np.isclose(np.linalg.norm(s), np.linalg.norm(d))
        assert sorted(np.linalg.norm(s, axis=0)[np.abs(s).sum(0) > 0]) == sorted(np.linalg.norm(d, axis=0)[[2, 7]])
        print("self-check ok")
    else:
        main()
