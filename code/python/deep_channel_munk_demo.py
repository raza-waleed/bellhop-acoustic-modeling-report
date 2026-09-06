"""
The deep-ocean Munk sound channel: a real, previously computed BELLHOP run.

This script does not run a new simulation. It reads waleed_ray2.shd, a
transmission-loss field genuinely computed with BELLHOP (Michael B.
Porter's Acoustics Toolbox, cited but not redistributed here) against the
canonical "Munk profile" deep-sound-channel sound-speed profile, at 50 Hz,
across a 51-point depth grid (0-5000 m) and a 1001-point range grid
(0-100 km). The .shd file and its companion waleed_ray2.env configuration
are original to this project; BELLHOP itself is third-party software used
here only as a local computation tool.

The parser in bellhop_io.read_shd() is an original implementation, written
from the Acoustics Toolbox's documented .shd format and independently
validated against this exact file: the recovered source depth (1000 m),
receiver-depth and range grids, and their spacing all match
waleed_ray2.env exactly, and the resulting transmission loss is physically
correct at two check points -- about 60 dB at 1 km range near the channel
axis (matching simple spherical spreading, 20*log10(1000)=60 dB), and
only about 79 dB at 100 km range at the same depth, dramatically better
than the ~100 dB spherical-spreading would predict. That gap is exactly
the deep sound channel (SOFAR) effect the Munk profile is designed to
demonstrate: sound trapped near the channel axis refracts back and forth
rather than spreading freely, and is the physical reason very-low-frequency
signals can be detected across ocean-basin distances.

Output (written to ../../figures/):
    munk_channel_tl.png -- transmission-loss field (range vs. depth)
"""
import numpy as np
import matplotlib.pyplot as plt

from common import FIG_DIR, CYAN, ORANGE, GRID, TEXT, style
from bellhop_io import read_shd

style()

SHD_FILE = "waleed_ray2.shd"
NSZ, NRZ, NR = 1, 51, 1001


def main():
    d = read_shd(SHD_FILE, nsz=NSZ, nrz=NRZ, nr=NR)
    pressure = d["pressure"][0]  # (depth, range)
    TL = -20 * np.log10(np.abs(pressure) + 1e-20)

    r_km = d["r"] / 1000.0
    z_m = d["zr"]

    fig, ax = plt.subplots(figsize=(11, 6))
    im = ax.pcolormesh(r_km, z_m, TL, shading="auto", cmap="viridis",
                        vmin=50, vmax=100)
    ax.invert_yaxis()
    ax.axhline(1200, color=ORANGE, linestyle="--", linewidth=1, alpha=0.8,
               label="sound-channel axis (~1200-1300 m)")
    ax.axhline(float(d["zs"][0]), color=CYAN, linestyle=":", linewidth=1.2,
               alpha=0.9, label=f"source depth ({int(d['zs'][0])} m)")
    ax.set_xlabel("range (km)")
    ax.set_ylabel("depth (m)")
    ax.set_title(f"{d['title']}, {d['freq']:.0f} Hz: transmission loss (dB re 1 m)\n"
                 "real BELLHOP output (waleed_ray2.shd), computed 2019")
    ax.legend(loc="lower right", facecolor="#0a0e14", edgecolor=GRID, labelcolor=TEXT)
    cbar = fig.colorbar(im, ax=ax, label="transmission loss (dB)")
    cbar.ax.yaxis.label.set_color(TEXT)
    cbar.ax.tick_params(colors=TEXT)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "munk_channel_tl.png", dpi=130)
    plt.close(fig)

    tl_1km = TL[10, np.argmin(np.abs(r_km - 1))]
    tl_100km = TL[10, np.argmin(np.abs(r_km - 100))]
    print(f"TL at 1 km, {z_m[10]:.0f} m depth:   {tl_1km:.1f} dB "
          f"(spherical spreading predicts {20*np.log10(1000):.1f} dB)")
    print(f"TL at 100 km, {z_m[10]:.0f} m depth: {tl_100km:.1f} dB "
          f"(spherical spreading predicts {20*np.log10(100000):.1f} dB)")
    print("saved munk_channel_tl.png")


if __name__ == "__main__":
    main()
