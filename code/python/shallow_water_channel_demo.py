"""
A custom shallow-water channel, and the impulse response it produces.

Unlike the deep Munk channel (previous two scripts), shalow1.env is not
a textbook reference case: it is a distinct, custom shallow-water
scenario -- 4 kHz, 60 m water depth, a near-isovelocity sound-speed
profile decreasing slightly with depth, a 1.5 m source and 5 m receiver
300 m apart. This script runs it through BELLHOP (cited, not
redistributed here) in ASCII-arrivals mode, then builds a channel impulse
response from the resulting multipath arrivals exactly as
waleedmainfile.m does: each arrival becomes a scaled, delayed impulse at
its travel time.

The arrivals parser in bellhop_io.read_arrivals_ascii() is an original
implementation, validated directly against this file's own numbers: the
zero-bounce, near-zero-angle arrival has a travel time of 0.1999 s at
300 m range, matching 300 m / 1500 m/s (the shallow-water sound speed
here) to within 0.1%.

Output (written to ../../figures/):
    shallow_water_arrivals.png -- arrival amplitude/delay stem plot and
                                   the resulting channel impulse response
"""
import subprocess
import numpy as np
import matplotlib.pyplot as plt

from common import FIG_DIR, CYAN, ORANGE, MAGENTA, GRID, TEXT, style
from bellhop_io import read_arrivals_ascii

style()

ENV_NAME = "shalow1"
FS = 96_000.0  # sampling rate for the reconstructed impulse response


def build_impulse_response(arrivals, fs):
    max_delay = max(a["delay_s"] for a in arrivals)
    n = int(np.ceil(max_delay * fs)) + 10
    h = np.zeros(n, dtype=complex)
    for a in arrivals:
        idx = int(round(a["delay_s"] * fs))
        phasor = a["amp"] * np.exp(1j * np.radians(a["phase_deg"]))
        h[idx] += phasor
    return h


def main():
    subprocess.run(["./bellhop.exe", ENV_NAME], check=True)
    d = read_arrivals_ascii(f"{ENV_NAME}.arr")
    arrivals = d["arrivals"]
    h = build_impulse_response(arrivals, FS)
    t_h = np.arange(len(h)) / FS

    fig, axes = plt.subplots(2, 1, figsize=(10, 7))
    delays = [a["delay_s"] for a in arrivals]
    amps = [a["amp"] for a in arrivals]
    axes[0].stem(delays, amps, linefmt=CYAN, markerfmt="o", basefmt=" ")
    axes[0].set_xlabel("arrival delay (s)")
    axes[0].set_ylabel("arrival amplitude")
    axes[0].set_title(f"BELLHOP arrivals: {d['freq']:.0f} Hz, "
                       f"{d['r'][0]:.0f} m range, {d['sd'][0]:.1f} m source / "
                       f"{d['rd'][0]:.0f} m receiver depth ({len(arrivals)} multipath arrivals)")

    axes[1].plot(t_h * 1000, np.abs(h), color=ORANGE)
    axes[1].set_xlabel("time (ms)")
    axes[1].set_ylabel("|h(t)|")
    axes[1].set_title("Reconstructed channel impulse response")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "shallow_water_arrivals.png", dpi=130)
    plt.close(fig)

    direct = min(arrivals, key=lambda a: a["delay_s"])
    expected = d["r"][0] / 1500.0
    print(f"{len(arrivals)} arrivals found")
    print(f"direct-path delay: {direct['delay_s']:.4f} s "
          f"(range/1500 m/s predicts {expected:.4f} s)")
    print("saved shallow_water_arrivals.png")

    np.save(FIG_DIR.parent / "code" / "python" / "shalow1_h.npy", h)


if __name__ == "__main__":
    main()
