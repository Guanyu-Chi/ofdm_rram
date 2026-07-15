#!/usr/bin/env python3
"""Calculate crossbar-level estimates and ADC dynamic-range checks."""

from pathlib import Path
import csv
import math

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "config" / "G_matrix_seed2026.csv"
OUT = ROOT / "results" / "performance_summary.csv"

ROWS = 128
COLS = 128
N = 4
STOP_S = 80e-9
V_LEVELS = [-0.3, -0.1, 0.3, 0.1]
G_ON = 1 / 1_000.0
G_OFF = 1 / 1_000_000.0


def load_g():
    vals = []
    with MATRIX.open() as f:
        for rec in csv.DictReader(f):
            vals.append(float(rec["conductance_s"]))
    return vals


def bits_for_range(span, lsb):
    if span <= 0 or lsb <= 0:
        return None
    return math.ceil(math.log2(span / lsb + 1))


def main():
    g = load_g()
    avg_v2 = sum(v * v for v in V_LEVELS) / len(V_LEVELS)
    avg_power_w = sum(gx * avg_v2 for gx in g)
    ops = ROWS * COLS * N * 2
    throughput_ops_s = ops / STOP_S
    energy_j = avg_power_w * STOP_S
    energy_per_op_j = energy_j / ops
    tops_w = throughput_ops_s / avg_power_w / 1e12 if avg_power_w > 0 else None

    sep_abs_max = ROWS * G_ON * 0.3
    mixed_abs_max = ROWS * G_ON * math.hypot(0.3, 0.3)
    lsb = G_OFF * 0.1
    sep_bits = bits_for_range(2 * sep_abs_max, lsb)
    mixed_bits = bits_for_range(2 * mixed_abs_max, lsb)
    adc_reduction_supported = sep_bits is not None and mixed_bits is not None and sep_bits < mixed_bits

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value", "unit", "scope", "status"])
        writer.writerow(["latency", f"{STOP_S:.3e}", "s", "defined as full transient/integration window", "configured"])
        writer.writerow(["operations_per_window", ops, "ops", "128 columns x 128 rows x 4 carriers x multiply-add factor 2", "derived"])
        writer.writerow(["throughput", f"{throughput_ops_s:.6e}", "ops/s", "crossbar read window", "derived"])
        writer.writerow(["average_crossbar_power", f"{avg_power_w:.6e}", "W", "resistor-level read-state estimate, no chip-level peripheral power", "estimated"])
        writer.writerow(["energy_per_window", f"{energy_j:.6e}", "J", "crossbar only", "estimated"])
        writer.writerow(["energy_per_op", f"{energy_per_op_j:.6e}", "J/op", "crossbar only", "estimated"])
        writer.writerow(["tops_per_w", f"{tops_w:.6e}", "TOPS/W", "crossbar only", "estimated"])
        writer.writerow(["separated_iq_abs_dynamic_range", f"{sep_abs_max:.6e}", "A", "worst-case one component", "derived_bound"])
        writer.writerow(["conventional_mixed_abs_dynamic_range", f"{mixed_abs_max:.6e}", "A", "worst-case mixed 16-QAM magnitude", "derived_bound"])
        writer.writerow(["separated_iq_adc_bits_bound", sep_bits, "bits", "same LSB assumption", "derived_bound"])
        writer.writerow(["conventional_mixed_adc_bits_bound", mixed_bits, "bits", "same LSB assumption", "derived_bound"])
        writer.writerow(["adc_reduction_supported_by_bound", adc_reduction_supported, "boolean", "must be confirmed with measured demod outputs", "conditional"])
        writer.writerow(["area_estimate", "【需用户确认】", "um^2", "requires confirmed 45nm selector dimensions and cell pitch", "blocked"])
    print(f"wrote {OUT}")
    print(f"adc_reduction_supported_by_bound={adc_reduction_supported}")


if __name__ == "__main__":
    main()
