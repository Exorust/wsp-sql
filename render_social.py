"""Render the neuron cloud from site/neurons.html as a square video and stills for social posts.

  uv run --with pillow --with numpy python render_social.py      (run viz_neurons.py first)

Writes social/neurons.mp4 (1080x1080, 12 s seamless loop), social/neurons_before.png, social/neurons_after.png.
Same data and projection as the web page; frames are drawn here because headless browsers mangle the fonts.
"""
import json, math, os, re, shutil, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

D = json.loads(re.search(r"const D=(\{.*?\});\n", open("site/neurons.html").read()).group(1))
FONT = os.path.expanduser("~/Library/Fonts/JetBrainsMono-{}.ttf")
f = lambda w, s: ImageFont.truetype(FONT.format(w), s)
TITLE, SUB, SMALL, LABEL = f("SemiBold", 54), f("Regular", 25), f("Regular", 21), f("Medium", 20)
BG, INK, MUTE, LINE = (18, 24, 32), (232, 236, 241), (154, 166, 179), (42, 53, 64)
PINK, BLUE, NEAR, FAR = (232, 107, 190), (95, 179, 209), (150, 160, 172), (52, 62, 74)
W = H = 1080; CX, CY, F = 540, 572, 300
S, FPS, T = 1 / 0.75, 30, 12.0
Y = lambda l: (l - 11.5) / 11.5 * 1.05

cloud = np.array(D["cloud"], dtype=float)  # layer, x, z


def proj(x, y, z, yaw, pitch=0.28):
    x1, z1 = x * math.cos(yaw) - z * math.sin(yaw), x * math.sin(yaw) + z * math.cos(yaw)
    y1, z2 = y * math.cos(pitch) - z1 * math.sin(pitch), y * math.sin(pitch) + z1 * math.cos(pitch)
    k = 3.2 / (3.2 + z2)
    return CX + x1 * F * k, CY - y1 * F * k, z2


def phase(t):  # hold before, move out, hold after, move back
    ease = lambda u: 2 * u * u if u < .5 else 1 - (-2 * u + 2) ** 2 / 2
    u = t / T
    return 0 if u < 1 / 6 else ease((u - 1 / 6) / .2) if u < 1 / 6 + .2 else 1 if u < .85 else 1 - ease((u - .85) / .15)


def frame(t):
    p, yaw = phase(t), -0.3 + 0.55 * math.sin(2 * math.pi * t / T)  # sway, so the edit direction stays sideways
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.text((60, 56), "Four neurons, one push", font=TITLE, fill=INK)
    d.text((60, 128), "Claude Fable 5.1 edited Qwen3.5-0.8B's weights by hand.", font=SUB, fill=MUTE)
    d.text((60, 162), "4 neurons. 4,083 weights. No training.", font=SUB, fill=MUTE)
    # layer ruler and the added direction
    a0, a1 = proj(-.95, Y(0), 0, yaw), proj(-.95, Y(23), 0, yaw)
    d.line([a0[:2], a1[:2]], fill=LINE, width=2)
    for l in (0, 5, 10, 15, 20, 23):
        q = proj(-.95, Y(l), 0, yaw); d.text((q[0] - 40, q[1] - 11), f"L{l}", font=SMALL, fill=MUTE)
    o, e = proj(0, Y(21.6), 0, yaw), proj(.72 * S, Y(21.6), 0, yaw)
    d.line([o[:2], e[:2]], fill=(110, 70, 100), width=2)
    d.text((e[0] + 8, e[1] - 12), "toward </think>", font=SMALL, fill=(190, 120, 170))
    # grey cloud, far dots first, shaded by depth
    pts = [proj(x * S, Y(l), z * S, yaw) for l, x, z in cloud]
    for px, py, pz in sorted(pts, key=lambda q: -q[2]):
        u = min(1, max(0, (0.6 - pz) / 1.2)); c = tuple(int(FAR[i] + (NEAR[i] - FAR[i]) * u) for i in range(3))
        d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=c)
    at = lambda n: (n["b"][0] + (n["a"][0] - n["b"][0]) * p, n["b"][1] + (n["a"][1] - n["b"][1]) * p)
    for n in D["paper"]:
        x, z = at(n); q = proj(x * S, Y(n["l"]), z * S, yaw); d.rectangle([q[0] - 2, q[1] - 2, q[0] + 2, q[1] + 2], fill=BLUE)
    marks = []
    for n in D["ours"]:
        x, z = at(n); q = proj(x * S, Y(n["l"]), z * S, yaw); q0 = proj(n["b"][0] * S, Y(n["l"]), n["b"][1] * S, yaw)
        d.line([q0[:2], q[:2]], fill=(150, 70, 125), width=2)
        d.rectangle([q[0] - 7, q[1] - 7, q[0] + 7, q[1] + 7], fill=PINK)
        marks.append((q, f"L{n['l']} #{n['c']}" + (f"  cos {n['a'][0]:.2f}" if p > .98 else "")))
    ly = -1e9
    for q, txt in sorted(marks, key=lambda m: m[0][1]):  # keep labels at least 26 px apart
        ly = max(q[1] - 12, ly + 26); tw = d.textlength(txt, font=LABEL)
        tx = q[0] + 14 if q[0] < W - tw - 40 else q[0] - tw - 14
        d.text((tx, ly), txt, font=LABEL, fill=PINK)
    # caption and legend
    cap = ("Each dot is one neuron, placed by the direction it writes." if p < .02 else
           "Each edit adds the same vector, toward </think>." if p < .98 else
           "The model now skips thinking. A bypass, not a repair.")
    d.text((60, 952), cap, font=SUB, fill=INK)
    x = 60
    for col, txt in ((PINK, "Fable edit, 4 neurons"), (BLUE, "MIT edit, 128 neurons"), (NEAR, "unchanged")):
        d.rectangle([x, 1007, x + 12, 1019], fill=col); d.text((x + 20, 1001), txt, font=SMALL, fill=MUTE); x += d.textlength(txt, font=SMALL) + 56
    d.text((W - 60 - d.textlength("wsp-sql.vercel.app", font=SMALL), 24), "wsp-sql.vercel.app", font=SMALL, fill=MUTE)
    return im


os.makedirs("social", exist_ok=True)
tmp = tempfile.mkdtemp()
n = int(T * FPS)
for i in range(n):
    frame(i / FPS).save(f"{tmp}/{i:04d}.png")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{tmp}/%04d.png", "-c:v", "libx264",
                "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", "social/neurons.mp4"], check=True)
shutil.rmtree(tmp)
frame(0.5).save("social/neurons_before.png"); frame(4.6).save("social/neurons_after.png")
frame(4.6).convert("RGB").save("social/neurons_poster.jpg", quality=88)
print("social/neurons.mp4", os.path.getsize("social/neurons.mp4"), "bytes,", n, "frames")
