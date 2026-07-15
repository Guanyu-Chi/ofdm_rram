#!/usr/bin/env python3
"""Compare separated I/Q and matched conventional mixed 16-QAM ADC dynamic range."""

from pathlib import Path
import csv
import math

ROOT = Path(__file__).resolve().parents[1]
SEP_WAVE = ROOT / "results" / "sim_run" / "psf" / "tbtran.tran.tran"
CONV_WAVE = ROOT / "results" / "mixed_baseline" / "psf" / "tbtran.tran.tran"
DR = ROOT / "results" / "dynamic_range_summary.csv"
MIXED_DR = ROOT / "results" / "mixed_baseline_dynamic_range_summary.csv"
ADC = ROOT / "results" / "adc_comparison.csv"
COLS = 128
ROWS = 128
CARRIERS = [250e6, 500e6, 750e6, 1e9]
LEVELS = [-0.3, -0.1, 0.3, 0.1]
G_ON = 1 / 1000.0
MATRIX = ROOT / "config" / "G_matrix_seed2026.csv"


def wl_levels(row):
    return [(LEVELS[(row + 2 * k) % 4], LEVELS[(row + 2 * k + 1) % 4]) for k in range(len(CARRIERS))]


def load_g():
    g = [[0.0 for _ in range(COLS)] for _ in range(ROWS)]
    with MATRIX.open() as f:
        for rec in csv.DictReader(f):
            g[int(rec["row"])][int(rec["col"])] = float(rec["conductance_s"])
    return g


def theory(g):
    out = {}
    for k in range(len(CARRIERS)):
        for c in range(COLS):
            out[(k, c, "I")] = sum(g[r][c] * wl_levels(r)[k][0] for r in range(ROWS))
            out[(k, c, "Q")] = sum(g[r][c] * wl_levels(r)[k][1] for r in range(ROWS))
    return out


def parse_final_outputs(path, prefixes):
    wanted = set()
    for c in range(COLS):
        for k in range(len(CARRIERS)):
            for prefix in prefixes:
                wanted.add(f"{prefix}_c{c:03d}_{k}")
    current = {}
    final = {}
    in_value = False
    with path.open() as f:
        for raw in f:
            line = raw.strip()
            if line == "VALUE":
                in_value = True
                continue
            if not in_value or not line.startswith('"'):
                continue
            key, val = line.rsplit(" ", 1)
            key = key.split('"')[1]
            if key == "time":
                if current:
                    final = current
                current = {}
            elif key in wanted:
                current[key] = float(val)
        if current:
            final = current
    return final


def main():
    g = load_g()
    ref = theory(g)
    sep = parse_final_outputs(SEP_WAVE, ["Icar", "Qcar"]) if SEP_WAVE.exists() else {}
    conv = parse_final_outputs(CONV_WAVE, ["ConvIcar", "ConvQcar"]) if CONV_WAVE.exists() else {}

    sep_measured = 0.0
    conv_measured = 0.0
    missing_sep = 0
    missing_conv = 0
    per_carrier = {k: {"sep": 0.0, "conv": 0.0} for k in range(len(CARRIERS))}
    for k in range(len(CARRIERS)):
        for c in range(COLS):
            si = sep.get(f"Icar_c{c:03d}_{k}")
            sq = sep.get(f"Qcar_c{c:03d}_{k}")
            ci = conv.get(f"ConvIcar_c{c:03d}_{k}")
            cq = conv.get(f"ConvQcar_c{c:03d}_{k}")
            if si is None or sq is None:
                missing_sep += 1
            else:
                local_sep = max(abs(si), abs(sq))
                sep_measured = max(sep_measured, local_sep)
                per_carrier[k]["sep"] = max(per_carrier[k]["sep"], local_sep)
            if ci is None or cq is None:
                missing_conv += 1
            else:
                local_conv = math.hypot(ci, cq)
                conv_measured = max(conv_measured, local_conv)
                per_carrier[k]["conv"] = max(per_carrier[k]["conv"], local_conv)

    sep_theory = ROWS * G_ON * 0.3
    conv_theory = ROWS * G_ON * math.hypot(0.3, 0.3)
    matrix_iq = max(abs(v) for v in ref.values())
    matrix_mixed = 0.0
    for k in range(len(CARRIERS)):
        for c in range(COLS):
            matrix_mixed = max(matrix_mixed, math.hypot(ref[(k, c, "I")], ref[(k, c, "Q")]))

    ratio = conv_measured / sep_measured if sep_measured else 0.0
    continuous_delta = math.log2(ratio) if ratio > 0 else 0.0
    experimental_status = "supported" if continuous_delta >= 0.5 and missing_sep == 0 and missing_conv == 0 else "not_supported"
    note = "matched baseline uses same crossbar, BPF, phase-window verification demodulator, and 80 ns integration window"

    for path in (DR, MIXED_DR):
        with path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["category", "separated_iq_bound", "conventional_mixed_bound", "unit", "status", "notes"])
            w.writerow(["theoretical_worst_case", f"{sep_theory:.12e}", f"{conv_theory:.12e}", "A", "derived", "all Ron worst case; conventional uses sqrt(I^2+Q^2) 16-QAM magnitude"])
            w.writerow(["matrix_specific_ideal", f"{matrix_iq:.12e}", f"{matrix_mixed:.12e}", "A", "derived_from_G_matrix", "ideal conductance-domain MVM for seed 2026"])
            w.writerow(["measured_matched_baseline", f"{sep_measured:.12e}", f"{conv_measured:.12e}", "V", "measured_from_separated_and_conventional_testbenches", note])

    with ADC.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value", "unit", "status", "notes"])
        w.writerow(["separated_measured_dynamic_range", f"{sep_measured:.12e}", "V", "measured", "max abs over Icar/Qcar nodes"])
        w.writerow(["conventional_mixed_measured_dynamic_range", f"{conv_measured:.12e}", "V", "measured", "max sqrt(ConvIcar^2+ConvQcar^2) over matched baseline nodes"])
        w.writerow(["measured_conventional_to_separated_ratio", f"{ratio:.12e}", "ratio", "derived", "ratio > 1 means conventional baseline has larger measured range"])
        w.writerow(["measured_continuous_bit_delta", f"{continuous_delta:.12e}", "bits", "derived", "log2(conventional/separated); one full ADC bit would require >= 1.0"])
        w.writerow(["experimental_adc_reduction_status", experimental_status, "boolean", experimental_status, "requires >= 0.5 continuous-bit margin for meaningful experimental support in this script"])
        w.writerow(["missing_separated_pairs", missing_sep, "count", "check", "expected 0"])
        w.writerow(["missing_conventional_pairs", missing_conv, "count", "check", "expected 0"])
        for k, freq in enumerate(CARRIERS):
            sep_k = per_carrier[k]["sep"]
            conv_k = per_carrier[k]["conv"]
            ratio_k = conv_k / sep_k if sep_k else 0.0
            delta_k = math.log2(ratio_k) if ratio_k > 0 else 0.0
            w.writerow([f"carrier_{int(freq)}_ratio", f"{ratio_k:.12e}", "ratio", "derived", f"continuous_bit_delta={delta_k:.12e}"])
    print(f"wrote {DR}")
    print(f"wrote {MIXED_DR}")
    print(f"wrote {ADC}")
    print(f"experimental_adc_reduction_status={experimental_status}")


if __name__ == "__main__":
    main()
