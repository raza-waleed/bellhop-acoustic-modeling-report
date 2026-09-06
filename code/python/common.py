"""Shared paths and plot styling for the BELLHOP report scripts."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = REPO_ROOT / "figures"
FIG_DIR.mkdir(exist_ok=True)

BG = "#0a0e14"
CYAN = "#22d3ee"
ORANGE = "#f59e0b"
MAGENTA = "#e879f9"
GRID = "#3a4553"
TEXT = "#c7d0dc"


def style():
    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
        "text.color": TEXT, "axes.edgecolor": GRID, "axes.labelcolor": TEXT,
        "xtick.color": TEXT, "ytick.color": TEXT, "font.size": 11,
    })
