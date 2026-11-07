"""The run loop: one editor call per turn (`claude -p` with Fable 5.1 by default, or `codex exec` with gpt-6-astra; tools off), exactly one ```python or ```forward block per
reply, a kernel over the weights, a forward-pass budget, a fresh conversation (handoff) every 40 turns.

usage: python harness/driver.py --run runs/wsp_p25 --passes 25 [--protocol nothink] [--editor fable|codex]
Resumable: state.json records everything; rerun the same command to continue."""
import argparse, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from kernel import Kernel
from forward import Forward

MAX_CODE_RUNS, HANDOFF_EVERY, MAX_TURNS = 300, 40, 600
PROTOCOLS = {
    "nothink": dict(thinking=False, max_tokens=1024, temp=0.0,
                    text="the chat template with thinking disabled (enable_thinking=False); greedy decoding (temperature 0); at most 1,024 new tokens"),
    "think": dict(thinking=True, max_tokens=8192, temp=0.0,
                  text="the chat template with thinking enabled (the model reasons between <think> and </think>, then answers); greedy decoding (temperature 0); at most 8,192 new tokens for reasoning and answer together"),
}


def ask(editor, prompt, run_dir, thread_id=None):
    """-> (answer_text, thread_id, usage, seconds). Retries on failure. editor: "fable" (claude CLI) or "codex" (gpt-6-astra)."""
    last = f"{run_dir}/last_message.md"
    if editor == "codex":
        env = dict(os.environ, CODEX_HOME=f"{HERE}/codex_home")
        cmd = ["codex", "exec"] + (["resume", thread_id] if thread_id else ["-C", run_dir]) + ["--json", "--skip-git-repo-check", "-o", last, "-"]
    else:  # tools off; no user settings, hooks, MCP servers, skills or auto-memory; same one-line system prompt as the codex config
        env = dict(os.environ, CLAUDE_CODE_DISABLE_AUTO_MEMORY="1")
        cmd = (["claude", "-p", "--model", "claude-fable-5-1", "--effort", "xhigh", "--tools", "", "--setting-sources", "", "--strict-mcp-config",
                "--disable-slash-commands", "--system-prompt", "Answer the user's request.", "--output-format", "json"]
               + (["--resume", thread_id] if thread_id else []))  # resume needs the same cwd, so cwd=run_dir below
    for attempt in range(6):
        t0 = time.time()
        p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, env=env, cwd=run_dir, timeout=3 * 3600)
        tid, usage, err, text = thread_id, None, [], ""
        if editor == "codex":
            for line in p.stdout.splitlines():
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                if ev.get("type") == "thread.started":
                    tid = ev["thread_id"]
                if ev.get("type") == "turn.completed":
                    usage = ev.get("usage")
                if ev.get("type") == "turn.failed" or ev.get("type") == "error":
                    err.append(json.dumps(ev)[:500])
            text = open(last).read() if os.path.exists(last) else ""
        else:
            try:
                d = json.loads(p.stdout)
                if d.get("is_error"):
                    err.append(json.dumps(d)[:500])
                else:
                    text, tid, usage = d.get("result") or "", d.get("session_id"), dict(d.get("usage") or {}, cost_usd=d.get("total_cost_usd"))
            except ValueError:
                err.append(p.stdout[-300:])
        if p.returncode == 0 and text.strip() and usage is not None:
            return text, tid, usage, time.time() - t0
        wait = 60 * (attempt + 1)
        print(f"  {editor} failed (rc={p.returncode}) {err[-1:] or p.stderr[-300:]}; retry in {wait}s", flush=True)
        time.sleep(wait)
    raise RuntimeError(f"{editor} kept failing")


def blocks(text):
    return re.findall(r"```(python|forward)\s*\n(.*?)```", text, flags=re.S)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True); ap.add_argument("--passes", type=int, default=25)
    ap.add_argument("--protocol", default="nothink", choices=list(PROTOCOLS))
    ap.add_argument("--model", default=f"{ROOT}/models/Qwen3.5-0.8B")
    ap.add_argument("--max-code-runs", type=int, default=MAX_CODE_RUNS)
    ap.add_argument("--editor", default="fable", choices=["fable", "codex"])
    a = ap.parse_args()
    run = os.path.abspath(a.run); work = f"{run}/work"; turns = f"{run}/turns"
    for d in (work, turns, f"{run}/requests"):
        os.makedirs(d, exist_ok=True)
    sp = f"{run}/state.json"
    st = json.load(open(sp)) if os.path.exists(sp) else dict(turn=0, passes_used=0, code_runs=0, thread=None, conv_turns=0,
                                                              handoffs=0, started=time.time(), protocol=a.protocol, passes=a.passes, editor=a.editor)
    proto = PROTOCOLS[st["protocol"]]
    fw = Forward(a.model, work, f"{ROOT}/practice/spider_train.jsonl", dict(thinking=proto["thinking"], max_tokens=proto["max_tokens"], temp=proto["temp"], batch=8 if proto["thinking"] else 16,
                                                                                                      gen_max=128 if proto["thinking"] else 512))  # a looping thinking pass of 128 takes ~45 min on the laptop
    kern = Kernel(a.model, work, python=sys.executable)
    task = open(f"{HERE}/prompt.md").read().format(PASSES=st["passes"], MODEL=a.model, WORK=work, PRACTICE=f"{ROOT}/practice",
                                                    PROTOCOL=proto["text"], MAX_TOKENS=proto["max_tokens"], MAX_CODE_RUNS=a.max_code_runs,
                                                    GEN_MAX=fw.cfg["gen_max"], GEN_MAX_BOTH=fw.cfg["gen_max"] // 2)
    if st["turn"] == 0:
        prompt = task
    else:  # resume = handoff
        prompt = None

    def handoff():
        notes = open(f"{work}/notes.md").read() if os.path.exists(f"{work}/notes.md") else "(no notes.md)"
        names, _ = fw.edit_manifest()
        st["thread"], st["conv_turns"], st["handoffs"] = None, 0, st["handoffs"] + 1
        return (task + f"\n\nHANDOFF. This is a fresh conversation; your previous one ended. State: {st['passes_used']} of {st['passes']} forward passes used, "
                f"{st['code_runs']} of {a.max_code_runs} code runs used, turn {st['turn']}. The kernel was restarted (variables lost); your edits in {work}/edited are kept: {names or 'none'}. "
                f"Your notes ({work}/notes.md):\n\n{notes}\n\nContinue from here.")

    if prompt is None:
        prompt = handoff()
    log = open(f"{run}/tool_calls.jsonl", "a")
    while st["turn"] < MAX_TURNS:
        st["turn"] += 1; st["conv_turns"] += 1
        td = f"{turns}/t{st['turn']:03d}"; os.makedirs(td, exist_ok=True)
        open(f"{td}/prompt.txt", "w").write(prompt)
        answer, st["thread"], usage, secs = ask(st.get("editor", "codex"), prompt, run, st["thread"])
        open(f"{td}/answer.md", "w").write(answer)
        json.dump(dict(turn=st["turn"], usage=usage, seconds=round(secs), thread=st["thread"]), open(f"{td}/run.json", "w"))
        bl = blocks(answer)
        done = st["passes_used"] >= st["passes"]
        print(f"turn {st['turn']}: {len(bl)} block(s) {[b[0] for b in bl]} passes {st['passes_used']}/{st['passes']} code {st['code_runs']} ({secs:.0f}s)", flush=True)
        if not bl:
            if done:
                open(f"{run}/final_answer.md", "w").write(answer); print("FINAL ANSWER received"); break
            prompt = "Your reply had no code block. Reply with exactly one block that starts with ```python or ```forward (the session ends only when all forward passes are used)."
        elif len(bl) > 1:
            prompt = f"Your reply had {len(bl)} code blocks. Send exactly one block per reply. Nothing was run."
        else:
            kind, code = bl[0]
            if kind == "python":
                if st["code_runs"] >= a.max_code_runs:
                    prompt = "Code run budget exhausted. Use forward passes or give your final answer (no code block)."
                else:
                    st["code_runs"] += 1
                    out, restarted = kern.run(code)
                    log.write(json.dumps(dict(turn=st["turn"], kind="python", code=code, out=out[:6000])) + "\n"); log.flush()
                    prompt = out + (f"\n[code runs used: {st['code_runs']}/{a.max_code_runs}]" if st["code_runs"] % 10 == 0 else "")
            else:
                if done:
                    prompt = "All forward passes are used. Make your final choice (the tensors in the edited folder are submitted) and reply without a code block."
                else:
                    try:
                        req = json.loads(code)
                    except ValueError as e:
                        req = None; out, counted = f"request failed (not counted): invalid JSON: {e}", False
                    if req is not None:
                        k = st["passes_used"] + 1
                        json.dump(req, open(f"{run}/requests/fwd_{k}.json", "w"), indent=1)
                        t0 = time.time(); out, counted = fw.handle(req, k)
                        print(f"  forward pass {k if counted else '(failed)'}: {time.time() - t0:.0f}s", flush=True)
                    if counted:
                        st["passes_used"] += 1
                    log.write(json.dumps(dict(turn=st["turn"], kind="forward", code=code, out=out[:6000], counted=counted)) + "\n"); log.flush()
                    prompt = out + f"\n[forward passes used: {st['passes_used']}/{st['passes']}]"
                    if st["passes_used"] >= st["passes"]:
                        prompt += "\nAll forward passes are now used. Make your final choice (the tensors in the edited folder are what is submitted) and reply without a code block, saying what you changed, the evidence for it and why you expect it to help."
        if st["conv_turns"] >= HANDOFF_EVERY and st["passes_used"] < st["passes"]:
            prompt = handoff()
        json.dump(st, open(sp, "w"), indent=1)
    kern.close(); json.dump(st, open(sp, "w"), indent=1)


if __name__ == "__main__":
    main()
