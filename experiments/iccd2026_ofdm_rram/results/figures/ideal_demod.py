#!/usr/bin/env python3
"""Stage-B ideal coherent demodulation on filter-only waveforms.

For each single-tone run, project each filter output onto cos/sin at that
channel's own measured LO frequency (I/Q), over a rectangular or Hann-weighted
integration window. Sweeps the window start over one period of the lowest
carrier to measure start-time sensitivity. LO phase reference is taken from
the channel's own ring (nsum fundamental), like a physical self-coherent mixer.

Outputs:
  ideal_demod_results.csv      one row per (stim, channel, window_kind)
  ideal_decision_margin.csv    per-channel margin summary (column-wise)
  ideal_demod_waveforms/       downsampled baseband product traces (CSV)
"""
from pathlib import Path
import argparse, csv
import numpy as np
from parse_filteronly_matrix import read_nut, ring_freq, CHANNELS, STIM_NSUM

CH_NSUM = {'250': 'XMOD250.nsum', '500': 'XMOD500.nsum',
           '750': 'XMOD750.nsum', '1g': 'XMOD1G.nsum'}

def lo_ref(tu, nsum_u, f):
    """Return unit phasor of the ring fundamental (LO phase reference)."""
    z = np.mean((nsum_u - nsum_u.mean()) * np.exp(-2j * np.pi * f * tu))
    return z / abs(z)

def demod(tu, vu, f, phasor, w):
    z = 2.0 * np.sum(vu * np.exp(-2j * np.pi * f * tu) * w) / np.sum(w)
    z = z / phasor  # rotate into the LO frame
    return z.real, z.imag, abs(z)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs', nargs='+', required=True,
                    help='stimlabel=path pairs, e.g. 250=filteronly_250_v3_ascii')
    ap.add_argument('--outdir', default='figures')
    ap.add_argument('--suffix', default='')
    ap.add_argument('--t0', type=float, default=120e-9)
    ap.add_argument('--win', type=float, default=20e-9)
    ap.add_argument('--sweep', type=float, default=4e-9)
    ap.add_argument('--sweepstep', type=float, default=0.25e-9)
    ap.add_argument('--fs', type=float, default=64e9, help='resample rate')
    args = ap.parse_args()
    outdir = Path(args.outdir)
    wavedir = outdir / 'ideal_demod_waveforms'
    wavedir.mkdir(exist_ok=True)

    stim_of_label = {'250': '250', '425': '500', '723': '750', '1229': '1g'}
    rows, sweeps = [], {}
    for spec in args.runs:
        tag, path = spec.split('=')
        stim_ch = stim_of_label[tag]
        names, a = read_nut(path)
        idx = {n: i for i, n in enumerate(names)}
        t = a[:, idx['time']]
        n0s = np.arange(0, args.sweep + 1e-15, args.sweepstep)
        tmax = args.t0 + args.sweep + args.win
        sel = (t >= args.t0 - 2e-9) & (t <= tmax + 2e-9)
        ts = t[sel]
        nu = int(round((tmax - args.t0 + 4e-9) * args.fs))
        tu_all = args.t0 - 2e-9 + np.arange(nu) / args.fs
        # per-channel measured LO freq + phase reference from its own ring
        fmeas, phref, vu_all, nsum_u = {}, {}, {}, {}
        for lbl, pn, nn in CHANNELS:
            ns = a[sel, idx[CH_NSUM[lbl]]]
            fmeas[lbl] = ring_freq(ts, ns)
            nsum_u[lbl] = np.interp(tu_all, ts, ns)
            v = a[sel, idx[pn]] - a[sel, idx[nn]]
            vu_all[lbl] = np.interp(tu_all, ts, v - v.mean())
        for dt0 in n0s:
            m = (tu_all >= args.t0 + dt0) & (tu_all < args.t0 + dt0 + args.win)
            tu, kinds = tu_all[m], {}
            kinds['rect'] = np.ones(m.sum())
            kinds['hann'] = np.hanning(m.sum())
            for lbl, pn, nn in CHANNELS:
                f = fmeas[lbl]
                ph = lo_ref(tu, nsum_u[lbl][m], f)
                for kind, w in kinds.items():
                    i, q, mag = demod(tu, vu_all[lbl][m], f, ph, w)
                    if abs(dt0) < 1e-15:
                        rows.append([tag, stim_ch, lbl, kind, f, i, q, mag,
                                     int(lbl == stim_ch)])
                    sweeps.setdefault((tag, lbl, kind), []).append((dt0, mag))
        # save downsampled baseband product trace (rect window, dt0=0)
        m = (tu_all >= args.t0) & (tu_all < args.t0 + args.win)
        with open(wavedir / f'baseband_stim{tag}{args.suffix}.csv', 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['time_s'] + [f'{c}_i' for c, _, _ in CHANNELS] +
                       [f'{c}_q' for c, _, _ in CHANNELS])
            step = 16
            tt = tu_all[m][::step]
            cols_i, cols_q = [], []
            for lbl, _, _ in CHANNELS:
                f0 = fmeas[lbl]
                ph = lo_ref(tu_all[m], nsum_u[lbl][m], f0)
                zz = 2 * vu_all[lbl][m] * np.exp(-2j * np.pi * f0 * tu_all[m]) / ph
                cols_i.append(zz.real[::step]); cols_q.append(zz.imag[::step])
            for k in range(len(tt)):
                w.writerow([f'{tt[k]:.6e}'] + [f'{c[k]:.6e}' for c in cols_i] +
                           [f'{c[k]:.6e}' for c in cols_q])
        print(f'run {tag}: f_meas = ' +
              ' '.join(f'{l}:{fmeas[l]/1e6:.2f}MHz' for l, _, _ in CHANNELS))

    with open(outdir / f'ideal_demod_results{args.suffix}.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['run', 'stim_channel', 'channel', 'window', 'f_demod_hz',
                    'i_v', 'q_v', 'mag_v', 'is_target'])
        w.writerows(rows)

    # column-wise decision margins + start sensitivity
    mrows = []
    for kind in ['rect', 'hann']:
        for lbl, _, _ in CHANNELS:
            own = [r for r in rows if r[3] == kind and r[2] == lbl and r[8] == 1]
            oth = [r for r in rows if r[3] == kind and r[2] == lbl and r[8] == 0]
            own_mag = own[0][7]
            worst = max(oth, key=lambda r: r[7])
            sw = np.array(sweeps[(own[0][0], lbl, kind)])
            drift = (sw[:, 1].max() - sw[:, 1].min()) / own_mag * 100
            mrows.append([kind, lbl, own_mag, worst[7], worst[0],
                          own_mag / worst[7], drift])
    with open(outdir / f'ideal_decision_margin{args.suffix}.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['window', 'channel', 'target_mag_v', 'worst_leak_mag_v',
                    'worst_leak_run', 'margin_x', 'start_drift_percent'])
        w.writerows(mrows)
    for r in mrows:
        print('win=%s ch=%-4s target=%.4e worst_leak=%.4e (run %s) margin=%.2fx drift=%.2f%%'
              % tuple(r[:1] + r[1:]))

if __name__ == '__main__':
    main()
