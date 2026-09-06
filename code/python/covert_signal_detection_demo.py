"""
Signal detection over the real shallow-water channel: covert vs. communication.

This is an original, from-scratch reproduction of waleedmainfile.m's core
methodology, not a line-by-line translation of it. That script convolves
two different test signals, referred to in its own comments as a "covert"
signal and a "communication" signal, through a BELLHOP-derived channel
impulse response, then recovers each by cross-correlating the channel
output against the known original signal (matched-filter detection,
exactly the Neyman-Pearson framework used elsewhere in this portfolio's
DSP report). The original MATLAB script's own definitions of its two test
signals were not present among the source materials for this report, so
two representative signals are designed here instead: a short spread-
spectrum-like pseudonoise burst for "covert" (a real low-probability-of-
intercept technique, since its energy is spread thinly across frequency
rather than concentrated at one tone), and a short QPSK-modulated burst
for "communication" (matching this portfolio's lake-trial report). Both
are passed through the exact same real channel impulse response computed
in shallow_water_channel_demo.py from BELLHOP's own multipath arrivals
for the shalow1 scenario, not an idealized or simulated channel.

Output (written to ../../figures/):
    covert_and_communication_detection.png -- both signals before/after
        the channel, and their matched-filter detection output
"""
import numpy as np
import matplotlib.pyplot as plt

from common import FIG_DIR, CYAN, ORANGE, MAGENTA, GRID, TEXT, style

style()

FS = 96_000.0
RNG = np.random.default_rng(7)


def make_covert_signal(n_chips=127, chip_rate=8000.0, fs=FS):
    """A short direct-sequence spread-spectrum burst: a +/-1 pseudonoise
    chip sequence modulating a low-amplitude carrier, spreading its energy
    thinly across bandwidth rather than concentrating it, the classic
    approach to a low-probability-of-intercept ("covert") signal."""
    chips = RNG.choice([-1.0, 1.0], size=n_chips)
    samples_per_chip = int(round(fs / chip_rate))
    baseband = np.repeat(chips, samples_per_chip)
    t = np.arange(len(baseband)) / fs
    fc = 20_000.0
    return 0.3 * baseband * np.cos(2 * np.pi * fc * t)


def make_communication_signal(n_symbols=64, symbol_rate=4000.0, fs=FS):
    """A short QPSK-modulated burst, consistent with this portfolio's
    lake-trial OFDM/QPSK report."""
    symbols = RNG.choice([1, -1, 1j, -1j], size=n_symbols)
    samples_per_symbol = int(round(fs / symbol_rate))
    baseband = np.repeat(symbols, samples_per_symbol)
    t = np.arange(len(baseband)) / fs
    fc = 20_000.0
    passband = np.real(baseband * np.exp(1j * 2 * np.pi * fc * t))
    return passband / np.max(np.abs(passband))


def matched_filter_score(record, template):
    corr = np.correlate(record, template, mode="valid")
    norm = np.linalg.norm(template) * np.sqrt(
        np.convolve(record ** 2, np.ones(len(template)), mode="valid")
    )
    norm[norm == 0] = 1e-12
    return np.abs(corr) / norm


def main():
    h = np.load("shalow1_h.npy")
    h_real = np.real(h)
    h_real = h_real / np.max(np.abs(h_real))

    covert = make_covert_signal()
    comm = make_communication_signal()

    covert_rx = np.convolve(covert, h_real)
    comm_rx = np.convolve(comm, h_real)

    covert_score = matched_filter_score(covert_rx, covert)
    comm_score = matched_filter_score(comm_rx, comm)

    fig, axes = plt.subplots(3, 2, figsize=(13, 9))
    t_tx_c = np.arange(len(covert)) / FS * 1000
    t_tx_m = np.arange(len(comm)) / FS * 1000
    axes[0, 0].plot(t_tx_c, covert, color=CYAN, linewidth=0.6)
    axes[0, 0].set_title("Covert signal (spread-spectrum burst), transmitted")
    axes[0, 1].plot(t_tx_m, comm, color=MAGENTA, linewidth=0.6)
    axes[0, 1].set_title("Communication signal (QPSK burst), transmitted")

    t_rx_c = np.arange(len(covert_rx)) / FS * 1000
    t_rx_m = np.arange(len(comm_rx)) / FS * 1000
    axes[1, 0].plot(t_rx_c, covert_rx, color=CYAN, linewidth=0.6)
    axes[1, 0].set_title("After the real shallow-water channel")
    axes[1, 1].plot(t_rx_m, comm_rx, color=MAGENTA, linewidth=0.6)
    axes[1, 1].set_title("After the real shallow-water channel")

    t_sc_c = np.arange(len(covert_score)) / FS * 1000
    t_sc_m = np.arange(len(comm_score)) / FS * 1000
    peak_c = np.argmax(covert_score)
    peak_m = np.argmax(comm_score)
    axes[2, 0].plot(t_sc_c, covert_score, color=ORANGE)
    axes[2, 0].axvline(t_sc_c[peak_c], color="white", linestyle="--", linewidth=1,
                        label=f"detected at t={t_sc_c[peak_c]:.2f} ms, score={covert_score[peak_c]:.2f}")
    axes[2, 0].set_title("Matched-filter detection score")
    axes[2, 0].set_xlabel("time (ms)")
    axes[2, 0].legend(facecolor="#0a0e14", edgecolor=GRID, labelcolor=TEXT, fontsize=8)
    axes[2, 1].plot(t_sc_m, comm_score, color=ORANGE)
    axes[2, 1].axvline(t_sc_m[peak_m], color="white", linestyle="--", linewidth=1,
                        label=f"detected at t={t_sc_m[peak_m]:.2f} ms, score={comm_score[peak_m]:.2f}")
    axes[2, 1].set_title("Matched-filter detection score")
    axes[2, 1].set_xlabel("time (ms)")
    axes[2, 1].legend(facecolor="#0a0e14", edgecolor=GRID, labelcolor=TEXT, fontsize=8)

    plt.tight_layout()
    plt.savefig(FIG_DIR / "covert_and_communication_detection.png", dpi=130)
    plt.close(fig)

    print(f"Covert signal:        peak detection score {covert_score[peak_c]:.3f} at t={t_sc_c[peak_c]:.3f} ms")
    print(f"Communication signal: peak detection score {comm_score[peak_m]:.3f} at t={t_sc_m[peak_m]:.3f} ms")
    print("saved covert_and_communication_detection.png")


if __name__ == "__main__":
    main()
