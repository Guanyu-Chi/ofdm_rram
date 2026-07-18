#!/usr/bin/env python3
"""Paper figures for the ICCD OFDM-RRAM experiment (v5 final dataset)."""
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from parse_filter_ac import read_ac

C = {'250':'#2a78d6','500':'#008300','750':'#e87ba4','1g':'#eda100'}
SEQ = ['#cde2fb','#b7d3f6','#9ec5f4','#86b6ef','#6da7ec','#5598e7',
       '#3987e5','#2a78d6','#256abf','#1c5cab','#184f95','#104281','#0d366b']
INK, INK2 = '#1a1a19', '#6b6a63'
CHN = ['250','500','750','1g']
LBL = {'250':'ch1 250 MHz','500':'ch2 500 MHz','750':'ch3 750 MHz','1g':'ch4 1000 MHz'}
plt.rcParams.update({'font.size':9,'axes.edgecolor':INK2,'axes.labelcolor':INK,
    'text.color':INK,'xtick.color':INK2,'ytick.color':INK2,'axes.linewidth':0.8,
    'font.family':'DejaVu Sans','figure.dpi':200})

# ---- Fig 1: leakage matrix heatmap ----
rows=list(csv.DictReader(open('figures/filteronly_leakage_matrix_v5.csv')))
M=np.array([[float(r[f'ch{c}_norm']) for c in CHN] for r in rows])
freqs=[float(r['stim_freq_mhz']) for r in rows]
fig,ax=plt.subplots(figsize=(4.2,3.4))
cmap=matplotlib.colors.LinearSegmentedColormap.from_list('seq',SEQ)
im=ax.imshow(M,cmap=cmap,vmin=0,vmax=1,aspect='equal')
for i in range(4):
    for j in range(4):
        v=M[i,j]
        ax.text(j,i,f'{v*100:.1f}%' if v<0.995 else '100%',ha='center',va='center',
                fontsize=8,color='#ffffff' if v>0.55 else INK)
ax.set_xticks(range(4),['ch1\n250','ch2\n500','ch3\n750','ch4\n1000'],fontsize=8)
ax.set_yticks(range(4),[f'{f:.0f} MHz' for f in freqs])
ax.set_xlabel('filter channel output'); ax.set_ylabel('stimulus carrier (measured)')
ax.set_title('Filter-only 4×4 leakage matrix (amp @ f0, normalized per row)',fontsize=9)
for s in ax.spines.values(): s.set_visible(False)
fig.colorbar(im,ax=ax,shrink=0.8,label='normalized amplitude')
fig.tight_layout(); fig.savefig('figures/fig_leakage_heatmap_v5.png',bbox_inches='tight'); plt.close(fig)

# ---- Fig 2: filter AC responses ----
names,a=read_ac('filter_ac_v2_ascii')
idx={n:i for i,n in enumerate(names)}
f=a[:,idx['freq']].real
fig,ax=plt.subplots(figsize=(5.4,3.2))
for c in CHN:
    H=np.abs(a[:,idx[f'bf{c}p']]-a[:,idx[f'bf{c}n']])
    ax.semilogx(f/1e6,20*np.log10(np.maximum(H,1e-9)),color=C[c],lw=1.6,label=LBL[c])
for fc in [250,500,750,1000]:
    ax.axvline(fc,color=INK2,lw=0.6,ls=':',alpha=0.6)
ax.set_xlim(50,3000); ax.set_ylim(-55,10)
ax.set_xlabel('frequency (MHz)'); ax.set_ylabel('|H| (dB, in-situ)')
ax.set_title('Filter bank frequency response (real buffer drive, Gilbert load)',fontsize=9)
ax.grid(alpha=0.25,lw=0.5)
ax.legend(frameon=False,fontsize=8,loc='lower left',ncol=2)
for lab,xx,yy in [('ch1',255,-1.5),('ch2',430,6),('ch3',690,8),('ch4',1210,5)]:
    ax.annotate(lab,(xx,yy),fontsize=8,color=C[{'ch1':'250','ch2':'500','ch3':'750','ch4':'1g'}[lab]],ha='center')
fig.tight_layout(); fig.savefig('figures/fig_filter_ac_response.png',bbox_inches='tight'); plt.close(fig)

# ---- Fig 3: ideal demod running integration (target channel per stim) ----
fig,axes=plt.subplots(2,2,figsize=(5.6,3.8),sharex=True)
tagof={'250':'250','425':'500','723':'750','1229':'1g'}
for k,(tag,ch) in enumerate(tagof.items()):
    ax=axes[k//2,k%2]
    rr=list(csv.DictReader(open(f'figures/ideal_demod_waveforms/baseband_stim{tag}_v5.csv')))
    t=np.array([float(r['time_s']) for r in rr])*1e9
    zi=np.array([float(r[f'{ch}_i']) for r in rr])
    zq=np.array([float(r[f'{ch}_q']) for r in rr])
    n=np.arange(1,len(t)+1)
    ax.plot(t-t[0],np.cumsum(zi)/n*1e3,color=C[ch],lw=1.6)
    ax.plot(t-t[0],np.cumsum(zq)/n*1e3,color=C[ch],lw=1.6,ls='--')
    ax.set_title(LBL[ch],fontsize=8.5,color=C[ch])
    ax.grid(alpha=0.25,lw=0.5)

for ax in axes[1]: ax.set_xlabel('time in window (ns)')
for ax in axes[:,0]: ax.set_ylabel('running mean (mV)')
fig.suptitle('Ideal coherent demodulation: running integration, solid = I, dashed = Q (20 ns window, start 160 ns)',fontsize=9)
fig.tight_layout(); fig.savefig('figures/fig_ideal_integration_v5.png',bbox_inches='tight'); plt.close(fig)

# ---- Fig 4: decision margins ideal vs Gilbert ----
mi={r['channel']:float(r['margin_x']) for r in csv.DictReader(open('figures/ideal_decision_margin_v5.csv')) if r['window']=='rect'}
mg={r['channel']:float(r['margin_x']) for r in csv.DictReader(open('figures/gilbert_channel_margin_v5.csv'))}
x=np.arange(4); w=0.34
fig,ax=plt.subplots(figsize=(4.6,3.0))
b1=ax.bar(x-w/2,[mi[c] for c in CHN],w,color='#2a78d6',label='ideal multiplier')
b2=ax.bar(x+w/2,[mg[c] for c in CHN],w,color='#008300',label='Gilbert (transistor)')
for b in (*b1,*b2):
    ax.text(b.get_x()+b.get_width()/2,b.get_height()+0.4,f'{b.get_height():.1f}',ha='center',fontsize=7.5)
ax.axhline(3,color='#e34948',lw=1,ls='--'); ax.text(3.52,3.3,'min 3.0',color='#e34948',fontsize=7.5,ha='right')
ax.set_xticks(x,[LBL[c] for c in CHN]); ax.set_ylabel('decision margin (target / max crosstalk)')
ax.set_title('Per-channel decision margin, ideal vs transistor demod',fontsize=9)
ax.legend(frameon=False,fontsize=8)
for s in ['top','right']: ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig('figures/fig_decision_margins_v5.png',bbox_inches='tight'); plt.close(fig)
print('wrote 4 figures')
