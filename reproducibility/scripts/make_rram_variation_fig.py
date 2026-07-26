#!/usr/bin/env python3
"""Accuracy vs RRAM conductance-variation sigma (var_only), showing networks
are robust to conductance variation; the circuit crosstalk dominates."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FIG = Path(__file__).resolve().parent
rows = list(csv.DictReader(open(FIG/'rram_variation_accuracy.csv')))
NETS = [('lenet5_mnist','LeNet5/MNIST','#2a78d6'),
        ('resnet20_mnist','ResNet20/MNIST','#008300'),
        ('vgg_cifar10','VGG8/CIFAR-10','#e87ba4'),
        ('vgg_cifar100','VGG8/CIFAR-100','#eda100')]
fig, ax = plt.subplots(figsize=(3.4, 2.0), dpi=600)
for key, lab, c in NETS:
    rs = [r for r in rows if r['network']==key and r['case']=='var_only']
    rs.sort(key=lambda r: float(r['sigma']))
    xs = [float(r['sigma'])*100 for r in rs]
    ys = [float(r['accuracy_mean']) for r in rs]
    ax.plot(xs, ys, 'o-', color=c, lw=1.3, ms=3.5, label=lab)
ax.set_xlabel('conductance variation $\\sigma$ (%)', fontsize=8)
ax.set_ylabel('accuracy (%)', fontsize=8)
ax.tick_params(labelsize=7.5)
ax.grid(alpha=0.25, lw=0.5)
ax.legend(frameon=False, fontsize=6.6, loc='lower left', ncol=2,
          handlelength=1.4, columnspacing=1.0, labelspacing=0.3)
for s in ['top','right']: ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(FIG/'fig_rram_variation.pdf', bbox_inches='tight')
fig.savefig(FIG/'fig_rram_variation.png', bbox_inches='tight')
print('wrote fig_rram_variation')
