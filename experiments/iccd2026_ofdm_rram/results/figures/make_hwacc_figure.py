#!/usr/bin/env python3
"""4.2 results figure: grouped bars, baseline vs measured crosstalk vs calibrated."""
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FIG = Path(__file__).resolve().parent
rows = list(csv.DictReader(open(FIG/'hw_aware_network_accuracy.csv')))
NETS = [('lenet5_mnist','LeNet5\nMNIST'), ('resnet20_mnist','ResNet20\nMNIST'),
        ('vgg_cifar10','VGG8\nCIFAR-10'), ('vgg_cifar100','VGG8\nCIFAR-100')]
NETS = [(k,l) for k,l in NETS if any(r['network']==k for r in rows)]
CASES = [('baseline','Software baseline','#2a78d6'),
         ('hw_full_DH','Measured crosstalk $D\\,H$','#e87ba4'),
         ('hw_cal_harmonic','+ harmonic calibrated','#008300')]
acc = {(r['network'], r['case']): float(r['accuracy_percent']) for r in rows}
INK, INK2 = '#1a1a19', '#6b6a63'
plt.rcParams.update({'font.size':8.5,'axes.edgecolor':INK2,'text.color':INK,
    'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK2,
    'font.family':'DejaVu Sans','figure.dpi':300})
x = np.arange(len(NETS)); w = 0.26
fig, ax = plt.subplots(figsize=(4.7, 2.6))
for i,(case,label,color) in enumerate(CASES):
    vals = [acc[(k,case)] for k,_ in NETS]
    b = ax.bar(x+(i-1)*w, vals, w, color=color, label=label)
    for r,v in zip(b,vals):
        ax.text(r.get_x()+r.get_width()/2, v+1.2, f'{v:.1f}', ha='center',
                fontsize=6.6, color=INK)
ax.set_xticks(x, [l for _,l in NETS], fontsize=8)
ax.set_ylabel('test accuracy (%)')
ax.set_ylim(0, 108)
ax.legend(frameon=False, fontsize=7.2, loc='upper right', ncol=1)
for sp in ['top','right']: ax.spines[sp].set_visible(False)
fig.tight_layout()
fig.savefig(FIG/'fig_hwacc_networks.pdf', bbox_inches='tight')
fig.savefig(FIG/'fig_hwacc_networks.png', bbox_inches='tight')
print('wrote fig_hwacc_networks')
