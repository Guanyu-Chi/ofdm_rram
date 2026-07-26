#!/usr/bin/env python3
"""End-to-end CIM transient waveform figure (v5 run, BL0 = single-LRS column).

Rendered near full single-column width and placed at \\linewidth so text stays
readable without zooming."""
import sys
sys.path.insert(0, 'figures')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from parse_filteronly_matrix import read_nut, ring_freq

INK='#1a1a19'; SIG='#0e7490'; LO='#b45309'; ACC='#2a78d6'; GRN='#008300'
names, a = read_nut('rramcim_4x4_v5_ascii')
idx = {n: i for i, n in enumerate(names)}
t = a[:, idx['time']] * 1e9
sel = (t >= 0) & (t <= 200)
ts = t[sel]
def sig(n): return a[sel, idx[n]]

fig, axes = plt.subplots(4, 1, figsize=(3.4, 3.9), sharex=True, dpi=600,
                         gridspec_kw={'hspace': 0.18})
panels = [('WL drive (row 4, 1 GHz)', sig('row4'), SIG),
          ('BL0 sensed (TIA out)', sig('tiaout'), SIG),
          ('Filter output, ch4', sig('bf1gp')-sig('bf1gn'), ACC),
          ('Gilbert baseband I/Q, ch4', None, GRN)]
TT = 8.0
for ax, (ttl, v, c) in zip(axes, panels):
    if v is not None:
        ax.plot(ts, v, color=c, lw=0.6)
    else:
        ax.plot(ts, sig('i1gp')-sig('i1gn'), color=GRN, lw=0.9)
        ax.plot(ts, sig('q1gp')-sig('q1gn'), color=ACC, lw=0.9)
    ax.text(0.015, 0.80, ttl, transform=ax.transAxes, fontsize=TT,
            weight='bold', color=INK,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.7))
    ax.tick_params(labelsize=7)
    ax.axvspan(160, 180, color='#0e7490', alpha=0.12, lw=0)
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    ax.margins(y=0.20)

# --- timing annotations consolidated above the top panel ---
top = axes[0]
top.annotate('coherent window\n160\u2013180 ns', xy=(170, 1.02), xytext=(170, 1.45),
             textcoords=top.get_xaxis_transform(),
             xycoords=top.get_xaxis_transform(), fontsize=7.5, color=SIG,
             ha='center', va='bottom',
             arrowprops=dict(arrowstyle='->', color=SIG, lw=0.9))

# --- baseband panel: inline I/Q labels + integrated value, no legend box ---
axes[3].text(202, (sig('q1gp')-sig('q1gn'))[-1], 'Q', fontsize=8.0,
             color=ACC, va='center', ha='left', weight='bold')
axes[3].text(202, (sig('i1gp')-sig('i1gn'))[-1], 'I', fontsize=8.0,
             color=GRN, va='center', ha='left', weight='bold')
s20 = (t >= 160) & (t <= 180)
di = (a[s20, idx['i1gp']]-a[s20, idx['i1gn']]).mean()
dq = (a[s20, idx['q1gp']]-a[s20, idx['q1gn']]).mean()
axes[3].text(0.015, 0.13, f'integrated $|z|$ = {np.hypot(di,dq)*1e3:.1f} mV',
             transform=axes[3].transAxes, fontsize=7.5, ha='left', color=INK,
             bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.75))

axes[3].set_xlabel('time (ns)', fontsize=8.0)
for ax in axes:
    ax.set_ylabel('V', fontsize=8.0)
fig.align_ylabels(axes)
fig.subplots_adjust(top=0.90, right=0.94)
fig.savefig('figures/fig_cim_endtoend_waveform.png', bbox_inches='tight')
fig.savefig('figures/fig_cim_endtoend_waveform.pdf', bbox_inches='tight')
print('wrote fig_cim_endtoend_waveform')
