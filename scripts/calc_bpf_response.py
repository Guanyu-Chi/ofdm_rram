#!/usr/bin/env python3
"""Calculate passive BPF response matrix for the generated carrier filters."""

from pathlib import Path
import csv
import math
import cmath

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "bpf_response.csv"
CARRIERS = [250e6, 500e6, 750e6, 1e9]
LREF = 1e-6
RLOAD = 1e6
Q_DESIGN = 20.0


def response(center, probe):
    cval = 1.0 / ((2 * math.pi * center) ** 2 * LREF)
    rval = 2 * math.pi * center * LREF / Q_DESIGN
    w = 2 * math.pi * probe
    z_r = rval
    z_l = 1j * w * LREF
    z_c = 1 / (1j * w * cval)
    h = z_r / (z_c + z_l + z_r)
    return abs(h)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["bpf_center_hz", "probe_hz", "gain_v_per_v", "relative_to_center_db", "status"])
        center_gains = {fc: response(fc, fc) for fc in CARRIERS}
        for fc in CARRIERS:
            for fp in CARRIERS:
                gain = response(fc, fp)
                rel = 20 * math.log10(gain / center_gains[fc]) if gain > 0 else -999
                writer.writerow([f"{fc:.0f}", f"{fp:.0f}", f"{gain:.12e}", f"{rel:.6f}", "derived_from_generated_RLC_values"])
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
