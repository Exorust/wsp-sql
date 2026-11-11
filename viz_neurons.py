"""Build site/neurons.html: a turning 3D cloud of Qwen3.5-0.8B MLP neurons, with the edited neurons moving.

  .venv/bin/python viz_neurons.py

Each dot is one MLP neuron, drawn by its output direction (its down_proj column, normalized).
Height = layer. x = cosine with the direction the Fable edit added (the four deltas are parallel).
z = first principal component of the sampled columns, after removing that direction.
Both horizontal axes use the same scale, so distances are true cosines.
ponytail: 300 random neurons per layer for the grey cloud; every edited neuron is drawn.
"""
import glob, json
import numpy as np
from safetensors import safe_open

BASE, PAPER, OURS = "models/Qwen3.5-0.8B", "models/Qwen3.5-0.8B-weight-space-programming", "release/fable_r1_edit_c.npz"
name = lambda l: f"model.language_model.layers.{l}.mlp.down_proj.weight"
unit = lambda m: m / np.linalg.norm(m, axis=-1, keepdims=True)

A = safe_open(glob.glob(f"{BASE}/*.safetensors")[0], "pt")
P = safe_open(glob.glob(f"{PAPER}/*.safetensors")[0], "pt")
W = {l: A.get_tensor(name(l)).float().numpy() for l in range(24)}

z = np.load(OURS)
ours = [(int(k.split(".")[3]), int(z[k][0]), z[k.replace("|cols", "|vals")][:, 0]) for k in z.files if k.endswith("|cols")]
delta = unit(np.stack([v - W[l][:, c] for l, c, v in ours]))
assert (delta @ delta.T).min() > 0.999, "edit columns no longer share one direction"
t = unit(delta.mean(0))

rng = np.random.default_rng(0)
cloud = [(l, unit(W[l][:, c])) for l in range(24) for c in rng.choice(3584, 300, replace=False)]
S = np.stack([v for _, v in cloud])
R = S - np.outer(S @ t, t)
pc = np.linalg.svd(R - R.mean(0), full_matrices=False)[2][0]
xz = lambda v: [round(float(v @ t), 4), round(float(v @ pc), 4)]

data = {
    "cloud": [[l, *xz(v)] for l, v in cloud],
    "ours": [{"l": l, "c": c, "b": xz(unit(W[l][:, c])), "a": xz(unit(v))} for l, c, v in ours],
    "paper": [],
}
for l in (15, 19):
    Pw = P.get_tensor(name(l)).float().numpy()
    for c in np.flatnonzero((Pw != W[l]).any(0)):
        data["paper"].append({"l": l, "c": int(c), "b": xz(unit(W[l][:, c])), "a": xz(unit(Pw[:, c]))})

HTML = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Edited Neurons</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<style>
:root{--paper:#F3F5F8;--ink:#16202A;--mute:#5B6774;--line:#D5DBE3;--dot:rgba(22,32,42,.32);--neuron:#C0398F;--other:#1F6F8B;
--sans:"Familjen Grotesk",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#121820;--ink:#E8ECF1;--mute:#9AA6B3;--line:#2A3540;--dot:rgba(232,236,241,.30);--neuron:#E86BBE;--other:#5FB3D1}}
:root[data-theme="dark"]{--paper:#121820;--ink:#E8ECF1;--mute:#9AA6B3;--line:#2A3540;--dot:rgba(232,236,241,.30);--neuron:#E86BBE;--other:#5FB3D1}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans)}
main{max-width:980px;margin:0 auto;padding:24px 16px 40px}
h1{font-size:clamp(24px,4vw,34px);margin:0 0 6px;letter-spacing:-.01em}
p{color:var(--mute);line-height:1.5;margin:0 0 14px;max-width:70ch}
.bar{display:flex;flex-wrap:wrap;gap:14px;align-items:center;font:12px var(--mono);color:var(--mute);margin:8px 0}
.k{display:inline-flex;align-items:center;gap:6px}.sw{width:10px;height:10px;display:inline-block}
button{font:12px var(--mono);color:var(--ink);background:none;border:1px solid var(--line);padding:6px 10px;cursor:pointer}
button:focus-visible{outline:2px solid var(--neuron);outline-offset:2px}
canvas{width:100%;height:min(72vh,640px);display:block;touch-action:none;cursor:grab;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
#state{min-width:9ch}
</style></head><body><main>
<h1>Four neurons, one push</h1>
<p>Each grey dot is one MLP neuron of Qwen3.5-0.8B (300 sampled per layer, 24 layers), placed by the direction it writes into the model. The Fable editor changed four of them, in layers 17 to 20. Each change adds the same direction, toward the <code>&lt;/think&gt;</code> token. Watch them leave the cloud. The paper's own released edit (blue, 128 neurons in layers 15 and 19) changes other directions, so on this axis it hardly moves.</p>
<div class="bar">
<span class="k"><span class="sw" style="background:var(--neuron)"></span>Fable edit, 4 neurons</span>
<span class="k"><span class="sw" style="background:var(--other)"></span>paper edit, 128 neurons</span>
<span class="k"><span class="sw" style="background:var(--dot)"></span>unchanged neurons</span>
<button id="play" aria-pressed="false">Pause</button><span id="state">before</span>
</div>
<canvas id="c" role="img" aria-label="Turning 3D point cloud of the model's neurons by layer. Four edited neurons in layers 17 to 20 move far out along the axis toward the end-of-thinking token, from cosine near 0 to between 0.44 and 0.69, while unchanged neurons stay between minus 0.07 and 0.07."></canvas>
<p style="margin-top:12px;font:12px var(--mono)">Drag to turn. Horizontal axes share one scale (cosine). x: alignment with the added direction. Depth: first principal component of the rest. Height: layer.</p>
</main>
<script>
const D=__DATA__;
const cv=document.getElementById('c'),g=cv.getContext('2d'),btn=document.getElementById('play'),st=document.getElementById('state');
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
let yaw=-0.6,pitch=0.28,playing=!reduce,clock=0,last=performance.now(),drag=null;
const css=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const S=1/0.75, Y=l=>(l-11.5)/11.5*1.05; // world: x,z in cosine units scaled, y by layer
function size(){const r=devicePixelRatio||1;cv.width=cv.clientWidth*r;cv.height=cv.clientHeight*r;g.setTransform(r,0,0,r,0,0)}
addEventListener('resize',size);size();
function proj(x,y,z){const W=cv.clientWidth,H=cv.clientHeight,f=Math.min(W,H)*0.42;
 const cy=Math.cos(yaw),sy=Math.sin(yaw),x1=x*cy-z*sy,z1=x*sy+z*cy;
 const cp=Math.cos(pitch),sp=Math.sin(pitch),y1=y*cp-z1*sp,z2=y*sp+z1*cp,k=3.2/(3.2+z2);
 return[W/2+x1*f*k,H/2-y1*f*k,z2]}
const ease=u=>u<.5?2*u*u:1-(-2*u+2)**2/2;
function phase(){const T=8,u=(clock%T)/T; // hold, move out, hold, move back
 if(u<.2)return 0;if(u<.4)return ease((u-.2)/.2);if(u<.8)return 1;return 1-ease((u-.8)/.2)}
function frame(now){const dt=Math.min(.05,(now-last)/1000);last=now;
 if(playing){clock+=dt;if(!drag)yaw+=dt*.25}
 const p=reduce&&!playing?1:phase();st.textContent=p<.02?'before':p>.98?'after':'editing';
 const W=cv.clientWidth,H=cv.clientHeight;g.clearRect(0,0,W,H);
 g.strokeStyle=css('--line');g.fillStyle=css('--mute');g.font='11px '+css('--mono');g.lineWidth=1;
 // layer axis
 const a0=proj(-.95,Y(0),0),a1=proj(-.95,Y(23),0);g.beginPath();g.moveTo(a0[0],a0[1]);g.lineTo(a1[0],a1[1]);g.stroke();
 for(const l of[0,5,10,15,20,23]){const q=proj(-.95,Y(l),0);g.fillText(l,q[0]-18,q[1]+4)}
 // direction arrow at layer 20
 const o=proj(0,Y(21.5),0),e=proj(.72*S,Y(21.5),0);g.beginPath();g.moveTo(o[0],o[1]);g.lineTo(e[0],e[1]);g.stroke();
 g.fillText('toward </think>',e[0]+6,e[1]+4);
 g.fillStyle=css('--dot');
 for(const[l,x,z]of D.cloud){const q=proj(x*S,Y(l),z*S);g.fillRect(q[0]-1,q[1]-1,2,2)}
 const draw=(arr,col,r,label)=>{g.fillStyle=col;for(const n of arr){
  const x=n.b[0]+(n.a[0]-n.b[0])*p,z=n.b[1]+(n.a[1]-n.b[1])*p,q=proj(x*S,Y(n.l),z*S);
  if(label){const q0=proj(n.b[0]*S,Y(n.l),n.b[1]*S);g.strokeStyle=col;g.globalAlpha=.5;g.beginPath();g.moveTo(q0[0],q0[1]);g.lineTo(q[0],q[1]);g.stroke();g.globalAlpha=1}
  g.fillRect(q[0]-r,q[1]-r,2*r,2*r);
  if(label)g.fillText('L'+n.l+' #'+n.c+(p>.98?'  cos '+n.a[0].toFixed(2):''),q[0]+r+5,q[1]+4)}};
 draw(D.paper,css('--other'),2,false);draw(D.ours,css('--neuron'),5,true);
 requestAnimationFrame(frame)}
requestAnimationFrame(frame);
btn.onclick=()=>{playing=!playing;btn.textContent=playing?'Pause':'Play';btn.setAttribute('aria-pressed',String(!playing))};
if(location.hash==='#after'){clock=4.6;playing=false} // ponytail: link straight to the edited state
if(!playing){btn.textContent='Play';btn.setAttribute('aria-pressed','true')}
cv.onpointerdown=e=>{drag=[e.clientX,e.clientY];cv.setPointerCapture(e.pointerId)};
cv.onpointermove=e=>{if(!drag)return;yaw+=(e.clientX-drag[0])*.008;pitch=Math.max(-1.2,Math.min(1.2,pitch+(e.clientY-drag[1])*.006));drag=[e.clientX,e.clientY]};
cv.onpointerup=()=>drag=null;
</script></body></html>
"""

open("site/neurons.html", "w").write(HTML.replace("__DATA__", json.dumps(data, separators=(",", ":"))))
print("site/neurons.html", len(data["cloud"]), "cloud", len(data["ours"]), "ours", len(data["paper"]), "paper")
