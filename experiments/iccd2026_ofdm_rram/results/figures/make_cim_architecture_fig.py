#!/usr/bin/env python3
"""Paper Fig: complete RRAM-CIM architecture, serpentine two-row layout."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
INK='#1a1a19'; SIG='#0e7490'; SIGBG='#e6f3f6'; LO='#b45309'; LOBG='#faf0e0'
DIG='#334155'; DIGBG='#eceff3'; CMP='#7a1f6e'; CMPBG='#f6e6f3'
fig,ax=plt.subplots(figsize=(7.0,3.6),dpi=300)
ax.set_xlim(0,100); ax.set_ylim(0,54); ax.axis('off')

def box(x,y,w,h,title,sub,fc,ec,ls='-'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.25',fc=fc,ec=ec,lw=1.0,linestyle=ls))
    ax.text(x+w/2,y+h*0.63,title,ha='center',va='center',fontsize=6.3,color=INK,weight='bold')
    ax.text(x+w/2,y+h*0.27,sub,ha='center',va='center',fontsize=5.1,color='#51616e')
def arr(x1,y1,x2,y2,c=SIG,ls='-'):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=7,lw=1.0,color=c,linestyle=ls))

# ---- top row: TX + array + sensing + conditioning + filters ----
box(1,44,11.5,7,'Digital input','2-bit codes b1 b0',DIGBG,DIG)
box(1,33,11.5,8.5,'Carrier + I/Q\nreferences','4 ring osc.\n250/500/750/1000 MHz',LOBG,LO)
box(16,38.5,12,8,'WL drivers','carrier modulation +\nharmonic low-pass',SIGBG,SIG)
arr(12.5,46,18,46.2); arr(12.5,38,16,41)
# crossbar
ax.add_patch(FancyBboxPatch((31,29.5),16.5,17,boxstyle='round,pad=0.25',fc=CMPBG,ec=CMP,lw=1.4,linestyle='--'))
ax.text(39.2,48.2,'4$\\times$4 RRAM crossbar (compact 1T1R)',ha='center',fontsize=6.2,weight='bold',color=CMP)
Gm=[[0,1,0,1],[0,1,1,0],[0,0,1,1],[1,0,1,0]]
for i in range(4):
    for j in range(4):
        ax.add_patch(plt.Circle((33.8+j*3.6,43.4-i*3.6),1.0,
            fc=('#7a1f6e' if Gm[i][j] else '#ffffff'),ec=CMP,lw=0.7))
ax.text(48.5,30.6,'$R_{on}$=1 k$\\Omega$\n$R_{off}$=1 M$\\Omega$',fontsize=5.0,color=CMP,ha='left')
arr(28,42.5,31,42.5)
box(51,38.5,13,8,'BL sensing','TIA on selected BL\n(low input impedance)',SIGBG,SIG)
arr(47.5,42.5,51,42.5)
box(67.5,38.5,13,8,'AC coupling +\ndiff. buffer','$V_{cm}$ bias, drives\nfour filters in parallel',SIGBG,SIG)
arr(64,42.5,67.5,42.5)
box(84,38.5,14.5,8,'Filter bank','Butterworth LP +\n3 LC band-select',SIGBG,SIG)
arr(80.5,42.5,84,42.5)

# ---- virtual-ground under crossbar (fills former blank) ----
box(31,19.5,16.5,6.5,'Virtual-ground cols','BL1--3: MVM readout\n(evaluation only)',DIGBG,DIG,':')
arr(35,29.3,35,26.4,DIG,':'); arr(43,29.3,43,26.4,DIG,':')

# ---- bottom row: RX chain flows right -> left ----
box(84,24,14.5,8,'Gilbert I/Q\nmixers','8 mixers per BL,\nself-coherent LO',SIGBG,SIG)
arr(91.2,38.5,91.2,32.4)
box(67.5,24,13,8,'20 ns coherent\nintegration','5/10/15/20 cycles,\nstart $\\geq$160 ns',SIGBG,SIG)
arr(84,28,80.9,28)
box(51,24,13,8,'Decision /\nnetwork output','post-processed I/Q',DIGBG,DIG,':')
arr(67.5,28,64.4,28)
# LO distribution
arr(6.7,33,6.7,15,LO,'--')
ax.plot([6.7,95],[15,15],color=LO,ls='--',lw=1.0)
ax.add_patch(FancyArrowPatch((95,15),(95,23.6),arrowstyle='-|>',mutation_scale=7,lw=1.0,color=LO,linestyle='--'))
ax.text(35,16.3,'self-coherent LO distribution (same ring oscillators)',fontsize=5.4,color=LO)

# ---- legend ----
lg=3.6
ax.add_patch(FancyBboxPatch((1,lg),3.2,2.6,boxstyle='round,pad=0.2',fc=SIGBG,ec=SIG,lw=1.0))
ax.text(5,lg+1.3,'transistor-level',fontsize=5.6,va='center')
ax.add_patch(FancyBboxPatch((15,lg),3.2,2.6,boxstyle='round,pad=0.2',fc=CMPBG,ec=CMP,lw=1.0,linestyle='--'))
ax.text(18.8,lg+1.3,'compact RRAM',fontsize=5.6,va='center')
ax.add_patch(FancyBboxPatch((29,lg),3.2,2.6,boxstyle='round,pad=0.2',fc=DIGBG,ec=DIG,lw=1.0,linestyle=':'))
ax.text(32.8,lg+1.3,'behavioral / eval-only',fontsize=5.6,va='center')
ax.add_patch(plt.Circle((52,lg+1.3),0.9,fc='#7a1f6e',ec=CMP,lw=0.7)); ax.text(53.4,lg+1.3,'$R_{on}$ cell',fontsize=5.6,va='center')
ax.add_patch(plt.Circle((62.5,lg+1.3),0.9,fc='#ffffff',ec=CMP,lw=0.7)); ax.text(63.9,lg+1.3,'$R_{off}$ cell',fontsize=5.6,va='center')
fig.savefig('figures/fig_cim_architecture.png',bbox_inches='tight')
fig.savefig('figures/fig_cim_architecture.pdf',bbox_inches='tight')
print('wrote fig_cim_architecture')
