# Code

Original Python scripts supporting the report's four figures, plus this
project's own BELLHOP configuration files and one real BELLHOP output
file. None of BELLHOP itself, its bundled MATLAB scripts, or the standard
Munk reference case are included here (see below).

## Scripts

- **`python/common.py`** - shared figure-output path and dark-theme
  matplotlib styling, matching the convention used across this portfolio.
- **`python/bellhop_io.py`** - original, from-scratch parsers for
  BELLHOP's three output formats:
  - `read_arrivals_ascii()` - the ASCII `.arr` arrivals format. Validated
    against `shalow1.arr`: the recovered direct-path delay (0.1999 s)
    matches simple range/sound-speed geometry (300 m / 1500 m/s = 0.2000 s)
    to within 0.1%.
  - `read_ray_trace()` - the ASCII `.ray` eigenray/ray-trace format.
    Validated against `waleedray.ray`: 11 of 20 recovered rays terminate
    within 2 km and 50 m of the eigenray target receiver, exactly the
    behavior expected of genuine eigenrays.
  - `read_shd(path, nsz, nrz, nr)` - the binary `.shd` transmission-loss
    field format. This BELLHOP build's header does not cleanly
    self-describe its own array dimensions, so the caller supplies them
    from the run's own `.env` file rather than relying on a guessed
    header layout. Validated against `waleed_ray2.shd`: the recovered
    source depth, receiver-depth grid, and range grid all match
    `waleed_ray2.env` exactly, and the resulting transmission loss is
    physically correct (60.0 dB at 1 km matching spherical spreading
    exactly; 79.2 dB at 100 km, far better than spherical spreading's
    100.0 dB, the expected deep-sound-channel effect).
- **`python/deep_channel_munk_demo.py`** - reads `waleed_ray2.shd`
  (already-computed, real 2019 output) and plots the transmission-loss
  field. Produces `figures/munk_channel_tl.png`.
- **`python/communication_frequency_demo.py`** - runs `waleedray.env`
  through BELLHOP (eigenray mode) and plots the resulting ray paths.
  Produces `figures/communication_frequency_eigenrays.png`. Requires
  `bellhop.exe` (see below).
- **`python/shallow_water_channel_demo.py`** - runs `shalow1.env` through
  BELLHOP (ASCII-arrivals mode), builds a channel impulse response from
  the real multipath arrivals, and plots both. Produces
  `figures/shallow_water_arrivals.png` and caches the impulse response to
  `shalow1_h.npy` for the next script. Requires `bellhop.exe`.
- **`python/covert_signal_detection_demo.py`** - an original
  reproduction of `waleedmainfile.m`'s detection methodology (not a
  translation of its code): builds a spread-spectrum ("covert") signal
  and a QPSK ("communication") signal, convolves each through the real
  shallow-water channel impulse response from the previous script, and
  detects each via matched filtering. Produces
  `figures/covert_and_communication_detection.png`. Requires
  `shalow1_h.npy` (already included) but not `bellhop.exe` itself.

## Running the BELLHOP-dependent scripts

`deep_channel_munk_demo.py` and `covert_signal_detection_demo.py` only
read files already included in this repository and need no external
tools beyond `numpy` and `matplotlib`. `communication_frequency_demo.py`
and `shallow_water_channel_demo.py` call BELLHOP directly and require a
copy of `bellhop.exe` (from Michael B. Porter's Acoustics Toolbox, not
included here, see [oalib-acoustics.org](https://oalib-acoustics.org/))
placed in `code/python/` alongside the scripts.

## What is cited but not included

- `bellhop.exe` and every plotting/file-reading MATLAB script bundled
  with the Acoustics Toolbox (`bellhop.m`, `plotray.m`, `plotarr.m`,
  `plotshd.m`, `plotssp.m`, `read_arrivals_asc0.m`, `read_env.m`,
  `read_env_core.m`) - all Michael B. Porter's own work, each credited
  "mbp" in its own source.
- `MunkB_ray.env`/`.prt`/`.ray` - the Acoustics Toolbox's own bundled
  demonstration of the Munk profile reference case.
- The "Munk profile" itself, a standard, publicly documented deep-ocean
  sound-speed profile (W. Munk, 1974).
- A related shallow-water scenario script explored alongside this
  project was developed jointly with a labmate and is not included here,
  since it is not solely original work.
- A generic DVB-T OFDM tutorial script found alongside the original
  BELLHOP working files is unrelated to underwater acoustics and was not
  used in this report.
