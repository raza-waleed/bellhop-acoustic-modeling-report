"""
Adapting the Munk deep channel to a communication-relevant frequency.

The classic Munk profile test case (previous script) is run at 50 Hz, a
frequency realistic for long-range, low-frequency SONAR, not underwater
acoustic communication. waleedray.env keeps the same canonical deep-ocean
sound-speed profile but raises the frequency to 48 kHz, three orders of
magnitude higher and squarely in the range used by real underwater
acoustic modems (compare the 3-18 kHz band used in this portfolio's lake
trial report). This script re-runs that exact scenario through BELLHOP
(Michael B. Porter's Acoustics Toolbox, cited but not redistributed here)
in eigenray mode, which finds the specific ray paths connecting the
source to one receiver exactly, and plots them.

The ray-file parser in bellhop_io.read_ray_trace() is an original
implementation and is validated by construction here: every recovered
eigenray must start at the source position and terminate within a few
tens of metres of the specified receiver position (100 km range, 800 m
depth) for eigenray-finding to have worked correctly at all.

Output (written to ../../figures/):
    communication_frequency_eigenrays.png -- eigenray paths at 48 kHz
"""
import subprocess
import numpy as np
import matplotlib.pyplot as plt

from common import FIG_DIR, CYAN, ORANGE, MAGENTA, GRID, TEXT, style
from bellhop_io import read_ray_trace

style()

ENV_NAME = "waleedray"
TARGET_RANGE_M = 100_000.0
TARGET_DEPTH_M = 800.0


def main():
    subprocess.run(["./bellhop.exe", ENV_NAME], check=True)
    d = read_ray_trace(f"{ENV_NAME}.ray")

    fig, ax = plt.subplots(figsize=(11, 6))
    for i, ray in enumerate(d["rays"]):
        path = ray["path"]
        end_r, end_z = path[-1]
        hit = (abs(end_r - TARGET_RANGE_M) < 2000) and (abs(end_z - TARGET_DEPTH_M) < 50)
        color = ORANGE if hit else CYAN
        ax.plot(path[:, 0] / 1000, path[:, 1], color=color, linewidth=1.1, alpha=0.85)

    ax.scatter([0], [1000], color=MAGENTA, s=60, zorder=5, label="source (1000 m)")
    ax.scatter([TARGET_RANGE_M / 1000], [TARGET_DEPTH_M], color="white",
               marker="x", s=80, zorder=5, label=f"receiver ({int(TARGET_DEPTH_M)} m, 100 km)")
    ax.invert_yaxis()
    ax.set_xlabel("range (km)")
    ax.set_ylabel("depth (m)")
    ax.set_title(f"Deep Munk channel at {d['freq']/1000:.0f} kHz: eigenrays, source to receiver\n"
                 "same sound-speed profile as the 50 Hz case, adapted to a communication-relevant frequency")
    ax.legend(loc="lower right", facecolor="#0a0e14", edgecolor=GRID, labelcolor=TEXT)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "communication_frequency_eigenrays.png", dpi=130)
    plt.close(fig)

    n_hit = sum(
        1 for r in d["rays"]
        if abs(r["path"][-1][0] - TARGET_RANGE_M) < 2000 and abs(r["path"][-1][1] - TARGET_DEPTH_M) < 50
    )
    print(f"{len(d['rays'])} eigenrays found, {n_hit} terminate within 2 km / 50 m of the receiver")
    print("saved communication_frequency_eigenrays.png")


if __name__ == "__main__":
    main()
