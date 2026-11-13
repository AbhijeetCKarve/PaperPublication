"""PRISMA 2020 flow diagram of the systematic review (Figure S1)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
fig, ax = plt.subplots(figsize=(8.6, 9.2))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

def box(x, y, w, h, text, fc="#ffffff", fs=8.6, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                linewidth=1.0, edgecolor="#333333", facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", linespacing=1.35)

def arrow(x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#333333", shrinkA=0, shrinkB=0))

# stage labels (left column)
for y, h, lab in [(80, 16, "Identification"), (36, 40, "Screening"), (4, 26, "Included")]:
    ax.add_patch(FancyBboxPatch((1, y), 6, h, boxstyle="round,pad=0.3,rounding_size=1.0",
                                linewidth=0.8, edgecolor="#333333", facecolor="#dde7f0"))
    ax.text(4, y + h / 2, lab, rotation=90, ha="center", va="center", fontsize=9, fontweight="bold")

# identification
box(10, 85, 52, 10, "Records identified from databases (n = 788)\n"
    "IEEE Xplore, primary string (n = 188)\n"
    "Lens.org, primary string (n = 124)\n"
    "Lens.org, secondary string (n = 476)", fc="#f3f6fa")
box(66, 85, 32, 10, "Records removed before screening\n\nDuplicates (DOI, then normalised title)\n(n = 93)")
arrow(62, 90, 66, 90)

# screening
box(10, 70, 52, 7, "Records screened by title, abstract and keywords\n(n = 695)", fc="#f3f6fa")
arrow(36, 85, 36, 77)
box(66, 70, 32, 7, "Excluded: no meta-learning or few-shot term\n(EC1, keyword pre-screen) (n = 466)")
arrow(62, 73.5, 66, 73.5)

box(10, 58, 52, 7, "Records assessed for publication type\n(n = 229)", fc="#f3f6fa")
arrow(36, 70, 36, 65)
box(66, 58, 32, 7, "Excluded: preprint, chapter, editorial, dataset,\nreport or thesis (EC4) (n = 29)")
arrow(62, 61.5, 66, 61.5)

box(10, 40, 52, 13, "Records read at title-and-abstract level\n(n = 200)", fc="#f3f6fa")
arrow(36, 58, 36, 53)
box(66, 38, 32, 17, "Excluded (n = 136)\n"
    "Meta-learning in another sense, or no\nanomaly/fault task (EC1) (n = 83)\n"
    "Image-only data (EC2) (n = 50)\n"
    "Survey, no method to classify (n = 2)\n"
    "Plain application of an existing method\n(EC3) (n = 1)", fs=8.2)
arrow(62, 46.5, 66, 46.5)

# included
box(10, 20, 52, 7, "Records retained from the searches\n(n = 64)", fc="#f3f6fa")
arrow(36, 40, 36, 27)
box(66, 20, 32, 7, "Added from the authors' reference lists,\nnot retrieved by either string (n = 2)")
arrow(66, 23.5, 62, 23.5)
box(10, 6, 52, 9, "Studies included in the review and coded on the\nfour taxonomy axes (n = 66)", fc="#dfe9d9", bold=True)
arrow(36, 20, 36, 15)

ax.text(50, 98.5, "", ha="center")
fig.tight_layout()
for ext in ("png", "pdf"):
    fig.savefig(ROOT / "figures" / f"fig_prisma_flow.{ext}", dpi=600 if ext == "png" else None, bbox_inches="tight")
print("wrote figures/fig_prisma_flow.png/.pdf")
