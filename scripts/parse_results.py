#!/usr/bin/env python3
"""Parse coherent demodulator outputs and compare against ideal MVM references."""

from pathlib import Path
import csv
import math

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "config" / "G_matrix_seed2026.csv"
WAVE = ROOT / "results" / "sim_run" / "psf" / "tbtran.tran.tran"
OUT = ROOT / "results" / "numerical_check.csv"
SUMMARY = ROOT / "results" / "numerical_summary.csv"
DR = ROOT / "results" / "dynamic_range_summary.csv"

ROWS = 128
COLS = 128
CARRIERS = [250e6, 500e6, 750e6, 1e9]
LEVELS = [-0.3, -0.1, 0.3, 0.1]
G_ON = 1 / 1_000.0
G_OFF = 1 / 1_000_000.0


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
    for k, _freq in enumerate(CARRIERS):
        for c in range(COLS):
            out[(k, c, "I")] = sum(g[r][c] * wl_levels(r)[k][0] for r in range(ROWS))
            out[(k, c, "Q")] = sum(g[r][c] * wl_levels(r)[k][1] for r in range(ROWS))
    return out


def parse_final_outputs():
    wanted = set()
    for c in range(COLS):
        for k in range(len(CARRIERS)):
            wanted.add(f"Icar_c{c:03d}_{k}")
            wanted.add(f"Qcar_c{c:03d}_{k}")
    in_value = False
    current_vals = {}
    final_vals = {}
    with WAVE.open() as f:
        for line in f:
            line = line.strip()
            if line == "VALUE":
                in_value = True
                continue
            if not in_value or not line.startswith('"'):
                continue
            key, val = line.rsplit(" ", 1)
            key = key.split('"')[1]
            if key == "time":
                if current_vals:
                    final_vals = current_vals
                current_vals = {}
            elif key in wanted:
                current_vals[key] = float(val)
        if current_vals:
            final_vals = current_vals
    return final_vals


def best_fit_gain(pairs):
    denom = sum(t * t for t, _m in pairs)
    if denom == 0:
        return 0.0
    return sum(t * m for t, m in pairs) / denom


def main():
    g = load_g()
    ref = theory(g)
    measured_nodes = parse_final_outputs() if WAVE.exists() else {}
    measured = {}
    for k in range(len(CARRIERS)):
        for c in range(COLS):
            measured[(k, c, "I")] = measured_nodes.get(f"Icar_c{c:03d}_{k}")
            measured[(k, c, "Q")] = measured_nodes.get(f"Qcar_c{c:03d}_{k}")

    gains = {}
    for k, freq in enumerate(CARRIERS):
        for comp in ("I", "Q"):
            pairs = [(ref[(k, c, comp)], measured[(k, c, comp)]) for c in range(COLS) if measured[(k, c, comp)] is not None]
            gains[(k, comp)] = best_fit_gain(pairs)

    abs_err_raw = []
    abs_err_norm = []
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["carrier_hz", "column", "component", "theory_a", "measured_demod_v", "fit_gain_v_per_a", "gain_normalized_measured_a", "abs_error_gain_normalized_a", "status"])
        for k, freq in enumerate(CARRIERS):
            for c in range(COLS):
                for comp in ("I", "Q"):
                    tv = ref[(k, c, comp)]
                    mv = measured[(k, c, comp)]
                    gain = gains[(k, comp)]
                    if mv is None or gain == 0:
                        writer.writerow([f"{freq:.0f}", c, comp, f"{tv:.12e}", "", f"{gain:.12e}", "", "", "missing_demod_output"])
                    else:
                        norm = mv / gain
                        err = abs(norm - tv)
                        abs_err_raw.append(abs(mv))
                        abs_err_norm.append(err)
                        writer.writerow([f"{freq:.0f}", c, comp, f"{tv:.12e}", f"{mv:.12e}", f"{gain:.12e}", f"{norm:.12e}", f"{err:.12e}", "measured_from_Icar_Qcar_nodes"])

    sep_theory_worst = ROWS * G_ON * 0.3
    conv_theory_worst = ROWS * G_ON * math.hypot(0.3, 0.3)
    matrix_iq_max = max(abs(v) for v in ref.values())
    matrix_mixed_max = 0.0
    measured_sep_max = 0.0
    measured_mixed_max = 0.0
    for k in range(len(CARRIERS)):
        for c in range(COLS):
            ti = ref[(k, c, "I")]
            tq = ref[(k, c, "Q")]
            matrix_mixed_max = max(matrix_mixed_max, math.hypot(ti, tq))
            mi = measured[(k, c, "I")]
            mq = measured[(k, c, "Q")]
            if mi is not None:
                measured_sep_max = max(measured_sep_max, abs(mi))
            if mq is not None:
                measured_sep_max = max(measured_sep_max, abs(mq))
            if mi is not None and mq is not None:
                measured_mixed_max = max(measured_mixed_max, math.hypot(mi, mq))

    with SUMMARY.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value", "status"])
        writer.writerow(["waveform_file", str(WAVE if WAVE.exists() else ""), "measured_from_Icar_Qcar_nodes" if measured_nodes else "missing_waveform"])
        writer.writerow(["max_abs_demod_output_v", f"{max(abs_err_raw) if abs_err_raw else 0:.12e}", "measured_from_Icar_Qcar_nodes"])
        writer.writerow(["max_gain_normalized_abs_error_a", f"{max(abs_err_norm) if abs_err_norm else 0:.12e}", "fit_gain_per_carrier_component"])
        writer.writerow(["mean_gain_normalized_abs_error_a", f"{sum(abs_err_norm)/len(abs_err_norm) if abs_err_norm else 0:.12e}", "fit_gain_per_carrier_component"])
        writer.writerow(["note", "Icar/Qcar are circuit-generated verification-demodulator outputs. Gain-normalized error uses per-carrier/component least-squares gain and is not an ADC claim.", "interpretation_required"])

    with DR.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "separated_iq_bound", "conventional_mixed_bound", "unit", "status", "notes"])
        writer.writerow(["theoretical_worst_case", f"{sep_theory_worst:.12e}", f"{conv_theory_worst:.12e}", "A", "derived", "all Ron worst case; conventional uses sqrt(I^2+Q^2) 16-QAM magnitude"])
        writer.writerow(["matrix_specific_ideal", f"{matrix_iq_max:.12e}", f"{matrix_mixed_max:.12e}", "A", "derived_from_G_matrix", "ideal conductance-domain MVM for seed 2026"])
        writer.writerow(["measured_demodulated", f"{measured_sep_max:.12e}", f"{measured_mixed_max:.12e}", "V", "measured_from_Icar_Qcar_nodes", "verification-demodulator output voltage; no conventional mixed circuit baseline yet"])
    print(f"wrote {OUT}")
    print(f"wrote {SUMMARY}")
    print(f"wrote {DR}")


if __name__ == "__main__":
    main()
