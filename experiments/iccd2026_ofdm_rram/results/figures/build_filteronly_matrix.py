#!/usr/bin/env python3
"""Combine per-stimulus filter-only CSVs into the 4x4 leakage matrix."""
import csv, sys
from pathlib import Path

STIMS = ['250', '425', '723', '1229']
CHANS = ['250', '500', '750', '1g']

def main():
    figdir = Path(__file__).resolve().parent
    suffix = sys.argv[1] if len(sys.argv) > 1 else ''
    rows = {}
    freqs = {}
    for s in STIMS:
        p = figdir / f'filteronly_matrix_stim{s}{suffix}.csv'
        if not p.exists():
            print(f'missing {p}, skipping', file=sys.stderr)
            continue
        with open(p) as f:
            for r in csv.DictReader(f):
                rows[(s, r['channel'])] = r
                freqs[s] = float(r['stim_freq_hz'])
    out = figdir / f'filteronly_leakage_matrix{suffix}.csv'
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['stim_label', 'stim_freq_mhz'] +
                   [f'ch{c}_amp_at_f0_mv' for c in CHANS] +
                   [f'ch{c}_norm' for c in CHANS])
        for s in STIMS:
            if s not in freqs:
                continue
            amps = [float(rows[(s, c)]['amp_at_f0_v']) * 1e3 for c in CHANS]
            norms = [float(rows[(s, c)]['norm_at_f0']) for c in CHANS]
            w.writerow([s, f'{freqs[s]/1e6:.2f}'] +
                       [f'{a:.5f}' for a in amps] + [f'{n:.4f}' for n in norms])
    print(f'wrote {out}')
    with open(out) as f:
        print(f.read())

if __name__ == '__main__':
    main()
