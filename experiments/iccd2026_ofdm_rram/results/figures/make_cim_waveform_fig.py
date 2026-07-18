#!/usr/bin/env python3
"""End-to-end CIM transient waveform figure (v4 run, BL0 = single-LRS column)."""
import sys
sys.path.insert(0,'figures')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from parse_filteronly_matrix import read_nut, ring_freq

INK='#1a1a19'; SIG='#0e7490'; LO='#b45309'; ACC='#2a78d6'; GRN='#008300'
names,a = read_nut('rramcim_4x4_v5_ascii')
idx={n:i for i,n in enumerate(names)}
t=a[:,idx['time']]*1e9
sel=(t>=0)&(t<=200)
ts=t[sel]
def sig(n): return a[sel,idx[n]]
fig,axes=plt.subplots(4,1,figsize=(7.0,4.6),sharex=True,dpi=300,
                      gridspec_kw={'hspace':0.12})
panels=[('WL drive (row 4, 1 GHz)', sig('row4'), SIG, 'V'),
        ('BL0 sensed (TIA output)', sig('tiaout'), SIG, 'V'),
        ('Filter output ch4 (diff)', sig('bf1gp')-sig('bf1gn'), ACC, 'V'),
        ('Gilbert baseband I/Q ch4 (diff)', None, GRN, 'V')]
for ax,(ttl,v,c,u) in zip(axes,panels):
    if v is not None:
        ax.plot(ts,v,color=c,lw=0.5)
    else:
        ax.plot(ts,sig('i1gp')-sig('i1gn'),color=GRN,lw=0.7,label='I')
        ax.plot(ts,sig('q1gp')-sig('q1gn'),color=ACC,lw=0.7,label='Q')
        ax.legend(frameon=False,fontsize=6,loc='upper center',ncol=2)
    ax.text(0.008,0.82,ttl,transform=ax.transAxes,fontsize=6.8,weight='bold',color=INK)
    ax.tick_params(labelsize=6)
    ax.axvspan(160,180,color='#0e7490',alpha=0.10,lw=0)
    for s in ['top','right']: ax.spines[s].set_visible(False)
axes[2].annotate('settling ($\\tau\\approx2Q/\\omega_0$)',xy=(30,axes[2].get_ylim()[1]*0.78),fontsize=6.2,color='#51616e',ha='left')
axes[3].annotate('measurement start 160 ns',xy=(160,axes[3].get_ylim()[0]*0.6),xytext=(110,axes[3].get_ylim()[0]*0.85),
                 fontsize=6.2,color=SIG,ha='right',va='bottom',
                 arrowprops=dict(arrowstyle='->',color=SIG,lw=0.8))
axes[3].text(170,axes[3].get_ylim()[1]*0.75,'20 ns coherent\nintegration',fontsize=6.2,color=SIG,ha='center')
# decision value annotation
s20=(t>=160)&(t<=180)
di=(a[s20,idx['i1gp']]-a[s20,idx['i1gn']]).mean(); dq=(a[s20,idx['q1gp']]-a[s20,idx['q1gn']]).mean()
axes[3].text(198,axes[3].get_ylim()[1]*0.55,f'integrated |z| = {np.hypot(di,dq)*1e3:.1f} mV',
             fontsize=6.4,ha='right',color=INK)
axes[3].set_xlabel('time (ns)',fontsize=7)
for ax in axes: ax.set_ylabel('V',fontsize=6)
fig.align_ylabels(axes)
fig.savefig('figures/fig_cim_endtoend_waveform.png',bbox_inches='tight')
fig.savefig('figures/fig_cim_endtoend_waveform.pdf',bbox_inches='tight')
print('wrote fig_cim_endtoend_waveform')
