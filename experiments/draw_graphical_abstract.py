"""Graphical abstract for the MAKE submission: 2200 x 1120 px (2:1, as MDPI recommends), PNG."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from draw_architectures import SVG, render_png, C

ROOT = Path(__file__).resolve().parents[1]
W, H = 1100, 560
s = SVG(W, H)

# headline
s.text(W / 2, 40, "Does meta-learning help detect anomalies in drifting industrial sensor streams?",
       size=24, weight="bold", anchor="middle", fill="#1a1a1a")
s.text(W / 2, 66, "66-paper review  →  benchmarking protocol  →  DAMAD, a drift-aware meta-adaptive detector  →  19,650 streaming runs on 8 public benchmarks",
       size=14, anchor="middle", fill="#444")

# three columns
cx, cy, cw, ch = 20, 90, 346, 420
# column 1: the problem and the gap
s.box(cx, cy, cw, ch, "model", title="The problem and the gap", title_size=15, body=(
    "Plants stream thousands of sensor readings,",
    "faults are rarely labelled, and the data keep",
    "drifting after deployment.",
    "",
    "Systematic review of 66 papers (2020–2025):",
    "every meta-learning detector is trained offline",
    "and never updated; every streaming detector",
    "does not meta-learn.",
))
s.text(cx + 18, cy + 262, "Taxonomy: paradigm × streaming capability", size=12.5, fill="#333")
s.grid(cx + 18, cy + 275, 4, 3, 52, 26, highlight=lambda c, r: (c, r) == (3, 2))
s.text(cx + 240, cy + 330, "the online", size=12.5, weight="bold", fill="#C0392B")
s.text(cx + 240, cy + 347, "meta-adaptive", size=12.5, weight="bold", fill="#C0392B")
s.text(cx + 240, cy + 364, "cell is empty", size=12.5, weight="bold", fill="#C0392B")
s.text(cx + 18, cy + 395, "No published method is few-shot, drift-aware, online.", size=11.5, fill="#555", style="italic")

# column 2: DAMAD loop
x2 = cx + cw + 11
s.box(x2, cy, cw, ch, "score", title="DAMAD: adapt only on real change", title_size=15, body=())
steps = [("1", "Score windows with a meta-learned VAE"),
         ("2", "Watch the model's residual with ADWIN"),
         ("3", "On a confirmed change: K gradient steps"),
         ("4", "Recalibrate the extreme-value threshold"),
         ("5", "Keep the old model if it still fits better")]
for i, (n, t) in enumerate(steps):
    y = cy + 66 + i * 58
    s.add(f'<circle cx="{x2 + 34}" cy="{y}" r="14" fill="{C["score"][1]}"/>')
    s.text(x2 + 34, y + 5, n, size=14, weight="bold", anchor="middle", fill="white")
    s.text(x2 + 58, y + 5, t, size=13, fill="#222")
    if i < len(steps) - 1:
        s.add(f'<line x1="{x2 + 34}" y1="{y + 14}" x2="{x2 + 34}" y2="{y + 44}" stroke="{C["score"][1]}" stroke-width="2"/>')
s.text(x2 + 18, cy + 372, "Past regimes are kept in memory and replayed", size=12, fill="#555", style="italic")
s.text(x2 + 18, cy + 390, "during meta-updates, so nothing is forgotten.", size=12, fill="#555", style="italic")

# column 3: the result
x3 = x2 + cw + 11
s.box(x3, cy, cw, ch, "good", title="What the 19,650 runs say", title_size=15, body=())
# bars: false alarms after drift
s.text(x3 + 18, cy + 62, "False alarms on normal steps after drift", size=13, weight="bold", fill="#222")
s.text(x3 + 18, cy + 86, "static / adapt-once", size=12.5, fill="#333")
s.bar(x3 + 150, cy + 74, 120, 16, 0.80, "#C0392B")
s.text(x3 + 278, cy + 87, "73–87 %", size=12.5, weight="bold", fill="#C0392B")
s.text(x3 + 18, cy + 112, "DAMAD", size=12.5, fill="#333")
s.bar(x3 + 150, cy + 100, 120, 16, 0.235, "#2E8B57")
s.text(x3 + 278, cy + 113, "17–30 %", size=12.5, weight="bold", fill="#2E8B57")
s.lines(x3 + 18, cy + 156, (
    "Recovers within 230–440 windows and has the",
    "best pooled F1 under all four drift patterns.",
    "",
    "Without drift, a static autoencoder is as good",
    "as any meta-learned detector on 6 of 8 datasets:",
    "the initialisation is not the bottleneck.",
    "",
    "Threshold recalibration and the residual-side",
    "gate carry the result; which meta-learner is",
    "used is secondary.",
), size=13, lh=19)

# footer
s.text(W / 2, H - 18, "SWaT · WADI · HAI 21.03 · SMAP · MSL · SMD · SKAB · PSM   |   5 seeds · 4 drift patterns · 8 baselines · 10 ablations   |   code and every table released",
       size=12.5, anchor="middle", fill="#555")

svg = ROOT / "figures" / "graphical_abstract.svg"
png = ROOT / "figures" / "graphical_abstract.png"
s.save(svg)
render_png(svg, png, W, H, scale=2.0)
print("wrote", png)
