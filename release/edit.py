"""Pack an editor's edit into a small .npz (only the changed columns), or apply such a file to the base checkpoint.

  python release/edit.py pack  runs/fable_think_p25_r1/work/edited_model release/fable_r1_edit_c.npz
  python release/edit.py apply release/fable_r1_edit_c.npz models/Qwen3.5-0.8B out/edited_model
ponytail: column edits only; every edit so far changed whole down_proj / o_proj columns.
"""
import os, shutil, sys
import numpy as np

ST = "model.safetensors-00001-of-00001.safetensors"


def pack(edited_dir, out, base="models/Qwen3.5-0.8B"):
    from safetensors import safe_open
    a, b = safe_open(f"{base}/{ST}", "pt"), safe_open(f"{edited_dir}/{ST}", "pt")
    d = {}
    for n in a.keys():
        x, y = a.get_tensor(n).float().numpy(), b.get_tensor(n).float().numpy()
        cols = np.flatnonzero((x != y).any(0))
        if len(cols): d[n + "|cols"] = cols; d[n + "|vals"] = y[:, cols]
    np.savez(out, **d); print(out, os.path.getsize(out), "bytes", {k: v.tolist() for k, v in d.items() if k.endswith("cols")})


def apply(npz, base, out):
    import torch
    from safetensors.torch import load_file, save_file
    d = np.load(npz); t = load_file(f"{base}/{ST}")
    for k in d.files:
        if k.endswith("|cols"):
            n = k[:-5]; w = t[n].float(); w[:, d[k]] = torch.from_numpy(d[n + "|vals"]); t[n] = w.to(torch.bfloat16)
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(base):
        if not f.endswith(".safetensors") and os.path.isfile(f"{base}/{f}"): shutil.copy(f"{base}/{f}", out)
    save_file(t, f"{out}/{ST}", metadata={"format": "pt"}); print("wrote", out)


if __name__ == "__main__":
    if sys.argv[1] == "pack": pack(sys.argv[2], sys.argv[3])
    else: apply(sys.argv[2], sys.argv[3], sys.argv[4])
