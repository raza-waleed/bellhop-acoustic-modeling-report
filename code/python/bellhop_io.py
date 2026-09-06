"""
Original, from-scratch Python readers for BELLHOP's plain-text and binary
output formats (.arr arrivals, .ray eigenrays/ray traces, .shd transmission-
loss fields). Written directly against this project's own sample output
files, not copied from the Acoustics Toolbox's own MATLAB readers
(read_arrivals_asc0.m, read_env_core.m, etc., all credited to M. B. Porter
and cited, not reproduced, in this report).

BELLHOP itself (bellhop.exe) is Michael B. Porter's Acoustics Toolbox
software; it is used here only as a local, unmodified, uncredited-output
generator, not redistributed in this repository.
"""
import struct
import numpy as np


def read_arrivals_ascii(path):
    """Parse a BELLHOP ASCII arrivals (.arr) file.

    Format (as produced by this BELLHOP build): a frequency/NSD/NRD/NR
    header line, then NSD source-depth values, NRD receiver-depth values,
    NR range values, then for each (range, receiver-depth, source-depth)
    triple: a count of arrivals followed by that many lines of
    (amplitude, phase_deg, delay_s, src_angle_deg, rcv_angle_deg,
    n_top_bounces, n_bottom_bounces).
    """
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]

    freq, nsd, nrd, nr = lines[0].split()
    nsd, nrd, nr = int(nsd), int(nrd), int(nr)
    idx = 1
    sd = [float(lines[idx + i]) for i in range(nsd)]
    idx += nsd
    rd = [float(lines[idx + i]) for i in range(nrd)]
    idx += nrd
    rng = [float(lines[idx + i]) for i in range(nr)]
    idx += nr

    arrivals = []
    for isd in range(nsd):
        # a summary block lists the arrival count for every (rd, r) pair
        # before the per-pair blocks themselves repeat it
        idx += nrd * nr
        for ird in range(nrd):
            for irr in range(nr):
                narr = int(lines[idx]); idx += 1
                for _ in range(narr):
                    vals = lines[idx].split(); idx += 1
                    arrivals.append({
                        "sd": sd[isd], "rd": rd[ird], "r": rng[irr],
                        "amp": float(vals[0]), "phase_deg": float(vals[1]),
                        "delay_s": float(vals[2]),
                        "src_angle_deg": float(vals[3]),
                        "rcv_angle_deg": float(vals[4]),
                        "n_top": int(vals[5]), "n_bot": int(vals[6]),
                    })
    return {"freq": float(freq), "sd": sd, "rd": rd, "r": rng, "arrivals": arrivals}


def read_ray_trace(path):
    """Parse a BELLHOP ASCII ray (.ray) file into a list of ray paths.

    Format (as produced by this BELLHOP build): a quoted title line, then
    frequency, number of launch angles, then Ndepth/top-depth/bottom-depth
    lines, then for each ray: a launch-angle line, a line with the number
    of points and top/bottom-boundary-type flags, then that many
    (range_m, depth_m) coordinate pairs.
    """
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]

    title = lines[0].strip("'").strip()
    freq = float(lines[1])
    n_launch = int(lines[2])
    # next 2 lines: source box depth range (min, max)
    idx = 5

    rays = []
    while idx < len(lines):
        launch_angle = float(lines[idx]); idx += 1
        header = lines[idx].split(); idx += 1
        npts = int(header[0])
        pts = []
        for _ in range(npts):
            r, z = lines[idx].split()[:2]
            pts.append((float(r), float(z)))
            idx += 1
        rays.append({"launch_angle_deg": launch_angle, "path": np.array(pts)})
    return {"title": title, "freq": freq, "n_launch": n_launch, "rays": rays}


def read_shd(path, nsz, nrz, nr):
    """Parse a BELLHOP binary shade (.shd) transmission-loss field file.

    This is a direct-access Fortran binary file: a small fixed-length
    header (record length, title, plot type, frequency) followed by the
    source-depth, receiver-depth, and range grids, then one record per
    (source depth, receiver depth) holding the complex acoustic pressure
    at every range, all as 4-byte (single-precision) values.

    The header's dimension-count fields were not cleanly self-describing
    for this particular (2019-era) BELLHOP build, so nsz/nrz/nr (source
    depths, receiver depths, ranges) are supplied by the caller from the
    corresponding .env file rather than auto-detected -- more robust than
    guessing at an ambiguous field layout. The record offsets used below
    (title, freq, then zs/zr/r grids at records 4/5/6, pressure data from
    record 7 on) were determined empirically against this project's own
    waleed_ray2.shd output and cross-checked against its .env file (grid
    sizes, source depth, depth/range spacing all matched exactly). This
    is an original implementation, not copied from the Acoustics
    Toolbox's own MATLAB reader.
    """
    with open(path, "rb") as f:
        raw = f.read()

    reclen = struct.unpack_from("i", raw, 0)[0] * 4  # record length in bytes
    def rec(n):
        return raw[n * reclen:(n + 1) * reclen]

    title = rec(0)[4:4 + 80].decode("ascii", errors="ignore").strip()
    freq0 = struct.unpack_from("f", rec(2), 0)[0]

    zs = np.frombuffer(rec(4), dtype="<f4", count=nsz)
    zr = np.frombuffer(rec(5), dtype="<f4", count=nrz)
    rr = np.frombuffer(rec(6), dtype="<f4", count=nr)

    header_recs = 7
    pressure = np.zeros((nsz, nrz, nr), dtype=complex)
    for isz in range(nsz):
        for irz in range(nrz):
            data = rec(header_recs + isz * nrz + irz)
            floats = np.frombuffer(data, dtype="<f4", count=2 * nr)
            pressure[isz, irz, :] = floats[0::2] + 1j * floats[1::2]

    return {
        "title": title, "freq": freq0, "zs": zs, "zr": zr, "r": rr,
        "pressure": pressure,
    }
