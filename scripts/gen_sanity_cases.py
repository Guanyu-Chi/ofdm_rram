#!/usr/bin/env python3
"""Generate 8x8 and 32x32 sanity matrices/netlists using the same read-state assumptions."""

from pathlib import Path
import csv
import math
import random

ROOT = Path(__file__).resolve().parents[1]
SEED = 2026
RON = 1_000.0
ROFF = 1_000_000.0
CARRIERS = [250e6, 500e6, 750e6, 1e9]
LEVELS = [-0.3, -0.1, 0.3, 0.1]


def pwl_wave(row):
    points = []
    dt = 0.25e-9
    steps = int(80e-9 / dt)
    comps = []
    for k, freq in enumerate(CARRIERS):
        comps.append((LEVELS[(row + 2 * k) % 4], LEVELS[(row + 2 * k + 1) % 4], freq))
    for n in range(steps + 1):
        t = n * dt
        v = sum(i * math.cos(2 * math.pi * f * t) + q * math.sin(2 * math.pi * f * t) for i, q, f in comps)
        points.append(f"{t:.12e} {v:.12e}")
    return " ".join(points)


def gen(size):
    rng = random.Random(SEED + size)
    matrix = ROOT / "config" / f"G_matrix_seed2026_{size}x{size}.csv"
    netlist = ROOT / "netlist" / f"clean_{size}x{size}_crossbar_sanity.scs"
    tb = ROOT / "tb" / f"tb_ofdm_qam_{size}x{size}_sanity.scs"
    states = []
    with matrix.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["row", "col", "state", "conductance_s"])
        for r in range(size):
            for c in range(size):
                state = "Ron" if rng.random() < 0.5 else "Roff"
                g = 1 / RON if state == "Ron" else 1 / ROFF
                states.append((r, c, state))
                writer.writerow([r, c, state, f"{g:.12e}"])
    with netlist.open("w") as f:
        f.write("// Sanity read-state OFDM/QAM-RRAM crossbar netlist\n")
        f.write("simulator lang=spectre\n")
        f.write("global 0 vdd\n")
        f.write("model nsel mos1 type=n vto=0.35 kp=250u lambda=0.05\n")
        f.write("VDD (vdd 0) vsource dc=1.0\n\n")
        for r in range(size):
            f.write(f"VWL{r:03d} (wl{r:03d} 0) vsource type=pwl wave=[ {pwl_wave(r)} ]\n")
        for c in range(size):
            f.write(f"RBLLOAD{c:03d} (bl{c:03d} 0) resistor r=1\n")
        for r, c, state in states:
            res = "1k" if state == "Ron" else "1meg"
            f.write(f"MSEL_r{r:03d}_c{c:03d} (n_r{r:03d}_c{c:03d} vdd wl{r:03d} wl{r:03d}) nsel w=45n l=45n\n")
            f.write(f"RRAM_r{r:03d}_c{c:03d} (n_r{r:03d}_c{c:03d} bl{c:03d}) resistor r={res}\n")
        for c in range(size):
            f.write(f"save bl{c:03d}\n")
    with tb.open("w") as f:
        f.write("// Sanity testbench, same carrier set as final 128x128 case\n")
        f.write("simulator lang=spectre\n")
        f.write(f"include \"../netlist/{netlist.name}\"\n")
        f.write("tbtran tran stop=80n maxstep=10p\n")
    print(f"wrote sanity case {size}x{size}")


def main():
    for size in (8, 32):
        gen(size)


if __name__ == "__main__":
    main()
