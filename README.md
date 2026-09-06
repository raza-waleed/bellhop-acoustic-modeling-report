# Ray-Tracing Simulation of Underwater Acoustic Channels

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22555196.svg)](https://doi.org/10.5281/zenodo.22555196)

A report connecting BELLHOP ray-tracing simulation to the rest of this
portfolio's real, measured underwater acoustics results: the deep-ocean
Munk sound channel (a real result computed in 2019), the same channel
adapted to a communication-relevant frequency, a custom shallow-water
scenario, and matched-filter signal detection over the channel impulse
response that scenario produces.

Open [`bellhop-acoustic-modeling-report.html`](bellhop-acoustic-modeling-report.html)
in a browser to read the report, or read it live at
[waleedraza.dev/underwater-acoustics/bellhop-modeling](https://waleedraza.dev/underwater-acoustics/bellhop-modeling/).

## What this is

BELLHOP (part of Michael B. Porter's Acoustics Toolbox) computes acoustic
ray paths and the resulting transmission loss, eigenrays, or channel
impulse response for a given sound-speed profile and geometry. This
report uses it for three scenarios, cites BELLHOP and the standard "Munk
profile" reference case it demonstrates by title and author without
reproducing either, and validates every result against an independent
physical or geometric expectation rather than trusting the tool's output
on its own:

- The deep-channel transmission loss (Section 3) matches simple
  spherical spreading at 1 km range (60.0 dB, exact) and shows the
  well-known reduced loss of the deep sound channel at 100 km range
  (79.2 dB vs. the 100.0 dB spherical spreading predicts).
- Every recovered eigenray at the communication-relevant frequency
  (Section 4) terminates within 2 km / 50 m of the specified receiver,
  the expected signature of genuine eigenrays.
- The shallow-water direct-path arrival delay (Section 5) matches
  simple range/speed geometry to within 0.1%.
- Both a covert and a communication test signal (Section 6) are
  correctly detected via matched filtering after passing through the
  real, BELLHOP-derived shallow-water channel impulse response.

See [`code/README.md`](code/README.md) for the original Python
implementation details, including how the BELLHOP binary/ASCII output
parsers were validated, and a full list of what is cited but
intentionally not included in this repository.

## Related reports in this portfolio

- [Underwater Acoustic Transducer & Hydrophone Systems](https://github.com/raza-waleed/acoustic-measurement-report) - tank characterization report
- [Underwater Acoustic OFDM/QPSK Communication](https://github.com/raza-waleed/underwater-acoustic-ofdm-lake-trial) - lake trial report
- [Digital Signal Processing for Underwater Acoustic Channels](https://github.com/raza-waleed/dsp-underwater-acoustics-report) - detection theory and array processing foundations

## Contents

```
bellhop-acoustic-modeling-report.html   the report
code/python/                            original demo scripts and BELLHOP configuration files (see code/README.md)
figures/                                generated figures used by the report
```

## Citing this work

To cite this specific archived release, cite the Zenodo record:

```bibtex
@software{raza2026bellhopraytracing,
  author    = {Raza, Waleed},
  title     = {raza-waleed/bellhop-acoustic-modeling-report: v1.0.0 - Ray-tracing report},
  year      = {2026},
  publisher = {Zenodo},
  version   = {v1.0.0},
  doi       = {10.5281/zenodo.22555196},
  url       = {https://doi.org/10.5281/zenodo.22555196}
}
```
