#!/usr/bin/env python3
"""Structural checks for generated OFDM/QAM-RRAM verification files."""

from pathlib import Path
import re
import csv

ROOT = Path(__file__).resolve().parents[1]
NETLIST = ROOT / "netlist" / "clean_128x128_crossbar.scs"
TB = ROOT / "tb" / "tb_ofdm_qam_128x128.scs"
OUT = ROOT / "results" / "structural_check.csv"
ROWS = 128
COLS = 128
CARRIERS = 4
PHASE_BINS = 16

CHECKS = [
    ("wordline_sources", r"^VWL[0-9]{3} ", ROWS, NETLIST),
    ("bitline_loads", r"^RBLLOAD[0-9]{3} ", COLS, NETLIST),
    ("rram_cells", r"^RRAM_r[0-9]{3}_c[0-9]{3} ", ROWS * COLS, NETLIST),
    ("selector_devices", r"^MSEL_r[0-9]{3}_c[0-9]{3} ", ROWS * COLS, NETLIST),
    ("bpf_paths_all_bl", r"^RBPF_c[0-9]{3}_[0-3] ", COLS * CARRIERS, TB),
    ("i_verification_demodulators", r"^EMIXI_c[0-9]{3}_[0-3]_[0-9]{2} ", COLS * CARRIERS * PHASE_BINS, TB),
    ("q_verification_demodulators", r"^EMIXQ_c[0-9]{3}_[0-3]_[0-9]{2} ", COLS * CARRIERS * PHASE_BINS, TB),
    ("i_phase_window_relays", r"^SMIXI_c[0-9]{3}_[0-3]_[0-9]{2} ", COLS * CARRIERS * PHASE_BINS, TB),
    ("q_phase_window_relays", r"^SMIXQ_c[0-9]{3}_[0-3]_[0-9]{2} ", COLS * CARRIERS * PHASE_BINS, TB),
    ("i_integrator_outputs", r"^CINTI_c[0-9]{3}_[0-3].*Icar_c[0-9]{3}_[0-3]", COLS * CARRIERS, TB),
    ("q_integrator_outputs", r"^CINTQ_c[0-9]{3}_[0-3].*Qcar_c[0-9]{3}_[0-3]", COLS * CARRIERS, TB),
]


def count(path, pattern):
    rx = re.compile(pattern)
    return sum(len(rx.findall(line)) for line in path.read_text().splitlines())


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    ok = True
    for name, pattern, expected, path in CHECKS:
        actual = count(path, pattern)
        passed = actual == expected
        ok = ok and passed
        rows.append([name, expected, actual, "pass" if passed else "fail", str(path.relative_to(ROOT))])
    text = TB.read_text()
    for freq in ["250000000", "500000000", "750000000", "1000000000"]:
        actual = text.count(f"freq={freq}")
        passed = actual == 2
        ok = ok and passed
        rows.append([f"reference_frequency_{freq}", 2, actual, "pass" if passed else "fail", "tb/tb_ofdm_qam_128x128.scs"])
    with OUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["check", "expected", "actual", "status", "file"])
        writer.writerows(rows)
    print(f"wrote {OUT}")
    print("overall=pass" if ok else "overall=fail")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
