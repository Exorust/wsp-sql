```python
# Direct logit attribution of (</think> minus '   ') margin at the '\n' positions: success text0 @1552 vs loop texts 4,5 at their appended-</think> positions
import torch
E = load("model.language_model.embed_tokens.weight")      # [V,1024]
gN = load("model.language_model.norm.weight")               # [1024]
ID_TC = 248069
ID_IND = tok.encode("   ").ids; print("indent ids", ID_IND)
ID_IND = ID_IND[0]
d = gN * (E[ID_TC] - E[ID_IND])   # margin direction
H = {l: np.load(f"{W}/fwd_7/hidden_L{l}.npy") for l in [20,22,23]}
M = {l: np.load(f"{W}/fwd_7/mlp_down_in_L{l}.npy") for l in [21,22,23]}
Wd = {l: load(f"model.language_model.layers.{l}.mlp.down_proj.weight") for l in [21,22,23]}  # [1024,3584]
Wd_orig = {l: load_original(f"model.language_model.layers.{l}.mlp.down_proj.weight") for l in [22,23]}
def attrib(n, q):
    h23 = torch.tensor(H[23][n,q].astype(np.float32)); rms = h23.pow(2).mean().sqrt()
    h20 = torch.tensor(H[20][n,q].astype(np.float32)); h22 = torch.tensor(H[22][n,q].astype(np.float32))
    mlp = {l: Wd_orig.get(l, Wd[l]) @ torch.tensor(M[l][n,q].astype(np.float32)) for l in [21,22,23]}
    tot = (h23 @ d)/rms
    parts = {"h20": (h20@d)/rms, "mlp21": (mlp[21]@d)/rms, "mlp22": (mlp[22]@d)/rms, "attn21+22": ((h22-h20-mlp[21]-mlp[22])@d)/rms,
             "mlp23": (mlp[23]@d)/rms, "attn23": ((h23-h22-mlp[23])@d)/rms}
    return float(tot), {k: round(float(v),2) for k,v in parts.items()}, float(rms)
print("text0 success @1552:", attrib(0,1552))
print("text4 loop @1296:", attrib(4,1296))
print("text5 loop @1241:", attrib(5,1241))
```