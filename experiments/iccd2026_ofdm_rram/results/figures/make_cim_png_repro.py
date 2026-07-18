#!/usr/bin/env python3
"""Reproduction of cim.png (architecture block diagram), widened layout:
longer arrows, wider crossbar, taller right-column blocks, roomier subtitles
and legend. Emits PNG and PDF."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

TEAL='#12808f'; TEALF='#ecf8f9'
PINK='#c23a90'; PINKF='#fbeaf5'
GRAY='#45586a'; GRAYF='#eef1f4'
ORANGE='#e17a28'; ORANGEF='#fef0e4'
PURP='#9c2199'; INK='#1b2733'; SUB='#3f4a55'
LS=1.55  # subtitle line spacing

W,H=1890,1060
fig,ax=plt.subplots(figsize=(9.3,5.30),dpi=200)   # wider aspect ~1.75
ax.set_xlim(0,W); ax.set_ylim(0,H); ax.invert_yaxis(); ax.axis('off')

def box(x,y,w,h,title,sub,ec,fc,ls='-',lw=2.2,tsz=10.5,ssz=8.5):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=6,rounding_size=16',
                 fc=fc,ec=ec,lw=lw,linestyle=ls,mutation_aspect=1))
    cx=x+w/2
    if sub:
        ax.text(cx,y+h*0.30,title,ha='center',va='center',fontsize=tsz,weight='bold',color=INK,linespacing=1.35)
        ax.text(cx,y+h*0.68,sub,ha='center',va='center',fontsize=ssz,color=SUB,linespacing=LS)
    else:
        ax.text(cx,y+h*0.5,title,ha='center',va='center',fontsize=tsz,weight='bold',color=INK,linespacing=1.35)

def arr(x1,y1,x2,y2,c=TEAL,ls='-',lw=2.6):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=18,
                 lw=lw,color=c,linestyle=ls,shrinkA=0,shrinkB=0))

# ---- top row ----
box(30,60,205,150,'Digital input','2-bit codes\n$b_1\\,b_0$',GRAY,GRAYF)
box(345,92,245,150,'WL drivers','carrier modulation +\nharmonic low-pass',TEAL,TEALF)
box(1170,150,180,210,'BL sensing','TIA on\nselected BL\n(low input\nimpedance)',TEAL,TEALF,tsz=10,ssz=8)
box(1400,150,205,210,'AC coupling +\ndiff. buffer','$V_{cm}$ bias, drives\nfour filters in\nparallel',TEAL,TEALF,tsz=9.5,ssz=8)
box(1655,150,205,210,'Filter bank','Butterworth LP+\n3 LC\nband-select',TEAL,TEALF,tsz=10,ssz=8)

# ---- carrier (orange), frequencies on two lines ----
box(30,265,235,205,'Carrier + I/Q\nreferences','4 ring oscillators\n250 / 500 /\n750 / 1000 MHz',ORANGE,ORANGEF,tsz=10.5,ssz=8.2)

# ---- crossbar (pink dashed), wider ----
CBx,CBw=660,375
box(CBx,30,CBw,450,'','',PINK,PINKF,ls=(0,(6,4)),lw=2.4)
cxc=CBx+CBw/2
ax.text(cxc,58,'4$\\times$4 RRAM crossbar',ha='center',va='center',fontsize=11.5,weight='bold',color=INK)
ax.text(cxc,92,'(compact 1T1R)',ha='center',va='center',fontsize=11,weight='bold',color=INK)
Gm=[[0,1,0,1],[0,1,1,0],[0,0,1,1],[1,0,1,0]]
step=78; gx0=cxc-1.5*step; gy0=155
xs=[gx0+j*step for j in range(4)]; ys=[gy0+i*step for i in range(4)]
for i in range(4): ax.plot([xs[0],xs[-1]],[ys[i],ys[i]],color='#333333',lw=1.3,zorder=1)
for j in range(4): ax.plot([xs[j],xs[j]],[ys[0],ys[-1]],color='#333333',lw=1.3,zorder=1)
for i in range(4):
    for j in range(4):
        ax.add_patch(Circle((xs[j],ys[i]),17,fc=(PURP if Gm[i][j] else 'white'),ec=PURP,lw=2.0,zorder=2))
ax.text(cxc,430,'$R_{\\mathrm{on}}$ = 1 k$\\Omega$',ha='center',fontsize=12.5,weight='bold',color=PURP)
ax.text(cxc,462,'$R_{\\mathrm{off}}$ = 1 M$\\Omega$',ha='center',fontsize=12.5,weight='bold',color=PURP)

# ---- virtual-ground ----
box(650,528,345,125,'Virtual-ground cols','BL1–3: MVM readout\n(evaluation only)',GRAY,GRAYF,ls=(0,(5,4)),lw=2.0,tsz=10.5,ssz=8.5)

# ---- bottom row (roomier subtitle line spacing via LS) ----
box(1560,650,300,175,'Gilbert I/Q\nmixers','8 mixers per BL,\nself-coherent LO',TEAL,TEALF,tsz=10.5,ssz=8.5)
box(1150,660,285,160,'20 ns coherent\nintegration','5 / 10 / 15 / 20 cycles,\nstart $\\geq$ 160 ns',TEAL,TEALF,tsz=10.5,ssz=8)
box(770,660,270,160,'Decision /\nnetwork output','post-processed I/Q\n(evaluation only)',GRAY,GRAYF,tsz=10.5,ssz=8.5)

# ---- arrows (longer, spanning wider gaps) ----
arr(235,135,345,150)
arr(190,275,345,205)
arr(590,165,660,180)
arr(1035,235,1170,240)
arr(1350,255,1400,255)
arr(1605,255,1655,255)
arr(1757,360,1757,650)
arr(1560,737,1435,737)
arr(1150,740,1040,740)
arr(720,482,720,528,GRAY,(0,(5,3)),3.0); arr(870,482,870,528,GRAY,(0,(5,3)),3.0)
# LO dashed
ax.add_patch(FancyArrowPatch((148,460),(148,865),arrowstyle='-',lw=2.4,color=ORANGE,linestyle=(0,(6,4))))
ax.add_patch(FancyArrowPatch((148,865),(1710,865),arrowstyle='-',lw=2.4,color=ORANGE,linestyle=(0,(6,4))))
ax.add_patch(FancyArrowPatch((1710,865),(1710,825),arrowstyle='-|>',mutation_scale=18,lw=2.4,color=ORANGE,linestyle=(0,(6,4))))
ax.text(929,905,'self-coherent LO distribution',ha='center',fontsize=13,weight='bold',color=ORANGE)

# ---- legend (wider, taller, more item spacing) ----
ax.add_patch(FancyBboxPatch((110,928),1640,124,boxstyle='round,pad=6,rounding_size=14',fc='white',ec=GRAY,lw=1.8))
ly=990
def lbox(x,ec,fc,ls,l1,l2):
    ax.add_patch(FancyBboxPatch((x,ly-28),56,56,boxstyle='round,pad=3,rounding_size=10',fc=fc,ec=ec,lw=2.0,linestyle=ls))
    ax.text(x+74,ly-16,l1,ha='left',va='center',fontsize=11.5,color=INK)
    ax.text(x+74,ly+18,l2,ha='left',va='center',fontsize=11.5,color=INK)
lbox(150,TEAL,TEALF,'-','transistor-level','(block)')
lbox(560,PINK,PINKF,(0,(5,3)),'compact','RRAM')
lbox(870,GRAY,GRAYF,(0,(4,3)),'behavioral /','eval-only')
ax.add_patch(Circle((1240,ly),24,fc=PURP,ec=PURP,lw=2)); ax.text(1278,ly-16,'$R_{\\mathrm{on}}$ cell',fontsize=11.5,va='center'); ax.text(1278,ly+18,'(1 k$\\Omega$)',fontsize=11.5,va='center')
ax.add_patch(Circle((1500,ly),24,fc='white',ec=PURP,lw=2)); ax.text(1538,ly-16,'$R_{\\mathrm{off}}$ cell',fontsize=11.5,va='center'); ax.text(1538,ly+18,'(1 M$\\Omega$)',fontsize=11.5,va='center')

fig.subplots_adjust(0,0,1,1)
fig.savefig('figures/cim_repro.png',dpi=200,bbox_inches='tight',pad_inches=0.05)
fig.savefig('figures/cim_repro.pdf',bbox_inches='tight',pad_inches=0.05)
print('wrote cim_repro.png / cim_repro.pdf')
