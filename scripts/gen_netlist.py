#!/usr/bin/env python3
"""Generate a clean 128x128 read-state crossbar netlist."""

from pathlib import Path
import csv
import math

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "config" / "G_matrix_seed2026.csv"
OUT = ROOT / "netlist" / "clean_128x128_crossbar.scs"

ROWS = 128
COLS = 128
STOP = "80n"
CARRIERS = [250e6, 500e6, 750e6, 1e9]
LEVELS = [-0.3, -0.1, 0.3, 0.1]


def read_matrix():
    states = {}
    with MATRIX.open() as f:
        for row in csv.DictReader(f):
            states[(int(row["row"]), int(row["col"]))] = row["state"]
    return states


def source_expr(row: int) -> str:
    parts = []
    for k, freq in enumerate(CARRIERS):
        i_level = LEVELS[(row + 2 * k) % len(LEVELS)]
        q_level = LEVELS[(row + 2 * k + 1) % len(LEVELS)]
        parts.append((i_level, q_level, freq))
    return parts


def pwl_wave(row: int) -> str:
    points = []
    dt = 0.125e-9
    steps = int(80e-9 / dt)
    comps = source_expr(row)
    for n in range(steps + 1):
        t = n * dt
        v = 0.0
        for i_level, q_level, freq in comps:
            v += i_level * math.cos(2 * math.pi * freq * t)
            v += q_level * math.sin(2 * math.pi * freq * t)
        points.append(f"{t:.12e} {v:.12e}")
    return " ".join(points)


def main() -> None:
    states = read_matrix()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        f.write("// Clean read-state OFDM/QAM-RRAM crossbar validation netlist\n")
        f.write("// Programmed cells are fixed conductance states during inference/read operation.\n")
        f.write("simulator lang=spectre\n")
        f.write("global 0 vdd\n")
        f.write("parameters vread_en=1.0 vdd_val=1.0\n\n")
        f.write("model nsel mos1 type=n vto=0.35 kp=250u lambda=0.05\n")
        f.write("VDD (vdd 0) vsource dc=vdd_val\n\n")
        for r in range(ROWS):
            f.write(f"VWL{r:03d} (wl{r:03d} 0) vsource type=pwl wave=[ {pwl_wave(r)} ]\n")
        f.write("\n")
        for c in range(COLS):
            f.write(f"RBLLOAD{c:03d} (bl{c:03d} 0) resistor r=1\n")
        f.write("\n")
        for r in range(ROWS):
            for c in range(COLS):
                state = states[(r, c)]
                res = "1k" if state == "Ron" else "1meg"
                f.write(f"MSEL_r{r:03d}_c{c:03d} (n_r{r:03d}_c{c:03d} vdd wl{r:03d} wl{r:03d}) nsel w=45n l=45n\n")
                f.write(f"RRAM_r{r:03d}_c{c:03d} (n_r{r:03d}_c{c:03d} bl{c:03d}) resistor r={res}\n")
        f.write("\n")
        for c in range(COLS):
            f.write(f"save bl{c:03d}\n")

    print(f"wrote {OUT}")
    print(f"rows={ROWS} cols={COLS} cells={ROWS * COLS}")


if __name__ == "__main__":
    main()
