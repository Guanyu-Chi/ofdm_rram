#!/usr/bin/env python3
"""Calculate read-window performance estimates for the OFDM-RRAM crossbar."""

from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "config" / "G_matrix_seed2026.csv"
OUT = ROOT / "results" / "performance_summary.csv"

ROWS = 128
COLS = 128
CARRIERS = 4
STOP_S = 80e-9
V_LEVELS = [-0.3, -0.1, 0.3, 0.1]


def load_conductances():
    vals = []
    with MATRIX.open() as f:
        for rec in csv.DictReader(f):
            vals.append(float(rec["conductance_s"]))
    return vals


def main():
    conductances = load_conductances()
    avg_v2 = sum(v * v for v in V_LEVELS) / len(V_LEVELS)
    avg_power_w = sum(g * avg_v2 for g in conductances)
    ops = ROWS * COLS * CARRIERS * 2
    throughput_ops_s = ops / STOP_S
    energy_j = avg_power_w * STOP_S
    energy_per_op_j = energy_j / ops
    tops_w = throughput_ops_s / avg_power_w / 1e12 if avg_power_w > 0 else None

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value", "unit", "scope", "status"])
        writer.writerow(["latency", f"{STOP_S:.3e}", "s", "full transient/read window", "configured"])
        writer.writerow(["operations_per_window", ops, "ops", "128 columns x 128 rows x 4 carriers x multiply-add factor 2", "derived"])
        writer.writerow(["throughput", f"{throughput_ops_s:.6e}", "ops/s", "crossbar read window", "derived"])
        writer.writerow(["average_crossbar_power", f"{avg_power_w:.6e}", "W", "resistor-level read-state estimate", "estimated"])
        writer.writerow(["energy_per_window", f"{energy_j:.6e}", "J", "resistor-level read-state estimate", "estimated"])
        writer.writerow(["energy_per_op", f"{energy_per_op_j:.6e}", "J/op", "resistor-level read-state estimate", "estimated"])
        writer.writerow(["tops_per_w", f"{tops_w:.6e}", "TOPS/W", "resistor-level read-state estimate", "estimated"])
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
