#!/usr/bin/env python3
"""Parse a Spectre nutascii filter-only run and summarize the four filter outputs.

Emits one CSV row per filter channel with mean, AC-RMS, half peak-to-peak
amplitude, and the dominant-tone frequency/amplitude from a uniform-resampled
FFT inside the analysis window. Intended to build the filter-only 4x4 leakage
matrix one stimulus at a time.
"""
from pathlib import Path
import argparse, csv
import numpy as np

CHANNELS = [('250', 'bf250p', 'bf250n'),
            ('500', 'bf500p', 'bf500n'),
            ('750', 'bf750p', 'bf750n'),
            ('1g',  'bf1gp',  'bf1gn')]

# stimulus label -> nsum node of the enabled DAC (to measure the actual tone freq)
STIM_NSUM = {'250': 'XMOD250.nsum', '425': 'XMOD500.nsum',
             '723': 'XMOD750.nsum', '1229': 'XMOD1G.nsum'}

def ring_freq(ts, v):
    ac = v - v.mean()
    z = np.where((ac[:-1] < 0) & (ac[1:] >= 0))[0]
    tz = ts[z] + (ts[z+1] - ts[z]) * (-ac[z]) / (ac[z+1] - ac[z])
    per = np.diff(tz)
    per = per[(per > 0.2 * np.median(per)) & (per < 2 * np.median(per))]
    return 1.0 / np.median(per)

def tone_amp(tu, vu, f0):
    ph = np.exp(-2j * np.pi * f0 * tu)
    return 2.0 * abs(np.mean(vu * ph))

def read_nut(path):
    names = []
    with open(path, errors='ignore') as f:
        for line in f:
            if line.startswith('Variables:'):
                toks = line.split()
                if len(toks) >= 3:
                    names.append(toks[2])
            elif line.startswith('Values:'):
                break
            elif names:
                toks = line.split()
                if len(toks) >= 2 and toks[0].isdigit():
                    names.append(toks[1])
        vals = np.fromiter((float(t) for chunk in f for t in chunk.split()), dtype=float)
    n = len(names)
    ncols = n + 1  # leading point index per row
    npts = len(vals) // ncols
    if len(vals) != npts * ncols:
        raise SystemExit(f'token count {len(vals)} not divisible by {ncols} (nvars={n})')
    a = vals.reshape(npts, ncols)[:, 1:]
    return names, a

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input')
    ap.add_argument('--out', required=True)
    ap.add_argument('--stim', required=True, help='stimulus label, e.g. 250')
    ap.add_argument('--start', type=float, default=120e-9)
    ap.add_argument('--stop', type=float, default=200e-9)
    ap.add_argument('--nfft', type=int, default=32768)
    args = ap.parse_args()

    names, a = read_nut(args.input)
    idx = {n: i for i, n in enumerate(names)}
    t = a[:, idx['time']]
    sel = (t >= args.start) & (t <= args.stop)
    ts, dur = t[sel], args.stop - args.start
    tu = np.linspace(args.start, args.stop, args.nfft, endpoint=False)

    f0 = ring_freq(ts, a[sel, idx[STIM_NSUM[args.stim]]])

    rows = []
    for label, pn, nn in CHANNELS:
        v = a[:, idx[pn]] - a[:, idx[nn]]
        vs = v[sel]
        mean = float(np.mean(vs))
        ac = vs - mean
        rms = float(np.sqrt(np.mean(ac**2)))
        halfpp = float(0.5 * (np.max(vs) - np.min(vs)))
        vu = np.interp(tu, ts, ac)
        spec = np.abs(np.fft.rfft(vu * np.hanning(args.nfft))) * 2 / (args.nfft * 0.5)
        freqs = np.fft.rfftfreq(args.nfft, d=dur / args.nfft)
        k = int(np.argmax(spec[1:])) + 1
        rows.append([args.stim, f0, label, mean, rms, halfpp,
                     float(freqs[k]), float(spec[k]), tone_amp(tu, vu, f0)])

    main_amp = max(r[8] for r in rows)
    for r in rows:
        r.append(r[8] / main_amp if main_amp > 0 else float('nan'))

    hdr = ['stim', 'stim_freq_hz', 'channel', 'mean_v', 'ac_rms_v', 'half_pp_v',
           'peak_freq_hz', 'peak_amp_v', 'amp_at_f0_v', 'norm_at_f0']
    with open(args.out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(hdr)
        w.writerows(rows)
    print(f'points={len(t)} window_points={int(sel.sum())} '
          f'window=[{args.start*1e9:.0f},{args.stop*1e9:.0f}]ns '
          f'stim_f0={f0/1e6:.2f}MHz wrote={args.out}')
    for r in rows:
        print('stim=%s ch=%s mean=%+.4e rms=%.4e halfpp=%.4e fpeak=%.4gMHz '
              'peak=%.4e amp@f0=%.4e norm@f0=%.4f'
              % (r[0], r[2], r[3], r[4], r[5], r[6] / 1e6, r[7], r[8], r[9]))

if __name__ == '__main__':
    main()
