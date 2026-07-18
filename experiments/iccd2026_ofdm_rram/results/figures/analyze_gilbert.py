#!/usr/bin/env python3
"""Stage-C: transistor Gilbert mixer metrics from existing filter-chain runs.

Settled window (default 160-180 ns). Per run and channel reports Gilbert
baseband I/Q (differential means), magnitude, conversion gain vs the filter
output fundamental, ripple (detrended AC rms in-window), pre-enable DC offset,
and LO feedthrough at the LO frequency on the baseband output.
"""
import sys, csv
import numpy as np
from parse_filteronly_matrix import read_nut, ring_freq, CHANNELS
from ideal_demod import CH_NSUM

VER = sys.argv[1] if len(sys.argv) > 1 else 'v2'
RUNS = [(tag, f'filteronly_{tag}_{VER}_ascii')
        for tag in ['250', '425', '723', '1229', '4tone']]
STIM_CH = {'250':'250','425':'500','723':'750','1229':'1g','4tone':'all'}
IQ = {'250':('i250p','i250n','q250p','q250n'),'500':('i500p','i500n','q500p','q500n'),
      '750':('i750p','i750n','q750p','q750n'),'1g':('i1gp','i1gn','q1gp','q1gn')}

def main():
    t0, t1, fs = 160e-9, 180e-9, 64e9
    rows = []
    for tag, path in RUNS:
        names, a = read_nut(path)
        idx = {n:i for i,n in enumerate(names)}
        t = a[:, idx['time']]
        s = (t >= t0) & (t <= t1)
        pre = (t >= 20e-9) & (t <= 34e-9)
        ts = t[s]
        tu = t0 + np.arange(int((t1-t0)*fs))/fs
        for lbl, pn, nn in CHANNELS:
            ip, inn, qp, qn = IQ[lbl]
            di = a[:, idx[ip]] - a[:, idx[inn]]
            dq = a[:, idx[qp]] - a[:, idx[qn]]
            f = ring_freq(ts, a[s, idx[CH_NSUM[lbl]]])
            bf = a[s, idx[pn]] - a[s, idx[nn]]
            bfu = np.interp(tu, ts, bf - bf.mean())
            abf = 2*abs(np.mean(bfu*np.exp(-2j*np.pi*f*tu)))
            mi, mq = di[s].mean(), dq[s].mean()
            mag = np.hypot(mi, mq)
            # ripple: detrended residual on I
            diu = np.interp(tu, ts, di[s])
            fit = np.polyval(np.polyfit(tu-t0, diu, 1), tu-t0)
            rip = (diu-fit).std()
            # LO feedthrough at f on baseband I
            lof = 2*abs(np.mean((diu-diu.mean())*np.exp(-2j*np.pi*f*tu)))
            off = di[pre].mean()
            conv = mag/abf if abf > 1e-6 else float('nan')
            rows.append([tag, STIM_CH[tag], lbl, f, mi, mq, mag, abf, conv,
                         rip, off, lof])
    hdr = ['run','stim','channel','f_lo_hz','i_mean_v','q_mean_v','mag_v',
           'bf_amp_v','conv_gain','ripple_rms_v','preenable_offset_v','lo_feedthrough_v']
    with open(f'figures/gilbert_c1_metrics_{VER}.csv','w',newline='') as fh:
        w = csv.writer(fh); w.writerow(hdr); w.writerows(rows)
    print('run    stim  ch    f[MHz]   I[mV]    Q[mV]   |z|[mV]  bf[mV]  conv   rip[mV] off[mV] LOft[mV]')
    for r in rows:
        print('%-6s %-5s %-4s %8.2f %+8.3f %+8.3f %8.3f %7.2f %6.3f %7.3f %+7.3f %7.3f'
              % (r[0],r[1],r[2],r[3]/1e6,r[4]*1e3,r[5]*1e3,r[6]*1e3,r[7]*1e3,r[8],r[9]*1e3,r[10]*1e3,r[11]*1e3))
    # per-channel margins at Gilbert level (column-wise across single-tone runs)
    print('\nGilbert-level channel margins (|z| own vs worst other run):')
    mrows=[]
    for lbl,_,_ in CHANNELS:
        own = [r for r in rows if r[2]==lbl and r[1]==lbl][0][6]
        others = [(r[6],r[0]) for r in rows if r[2]==lbl and r[1] not in (lbl,'all')]
        wv,wr = max(others)
        four = [r for r in rows if r[2]==lbl and r[0]=='4tone'][0][6]
        mrows.append([lbl, own, wv, wr, own/wv, four, four/own])
        print(f'ch{lbl:4s} own={own*1e3:7.3f}mV worst_leak={wv*1e3:7.3f}mV ({wr}) margin={own/wv:6.2f}x  4tone={four*1e3:7.3f}mV ratio={four/own:.3f}')
    with open(f'figures/gilbert_channel_margin_{VER}.csv','w',newline='') as fh:
        w=csv.writer(fh)
        w.writerow(['channel','own_mag_v','worst_leak_mag_v','worst_leak_run','margin_x','fourtone_mag_v','fourtone_over_single'])
        w.writerows(mrows)

if __name__ == '__main__':
    main()
