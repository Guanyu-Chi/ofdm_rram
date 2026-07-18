#!/usr/bin/env python3
"""RRAM conductance-variation inference sweep on real trained networks.

Complements the phase/crosstalk study: each mapped conductance (weight
magnitude) is perturbed by an independent zero-mean Gaussian relative error
(1+N(0,sigma)), clamped nonnegative, redrawn per trial, averaged over trials.
Reported alone and jointly with the measured, harmonic-calibrated hardware
crosstalk model (D H with the deterministic 250->750 term removed).

Reuses the loaders / checkpoints / injection hook from hw_aware_network_eval.
"""
import argparse, csv, sys, time, copy
from pathlib import Path
import numpy as np
import torch

FIG = Path(__file__).resolve().parent
sys.path.insert(0, str(FIG))
import hw_aware_network_eval as hw

def perturb_weights(net, sigma, gen):
    """In-place multiplicative Gaussian on conv/linear weight magnitudes."""
    saved = {}
    for name, p in net.named_parameters():
        if p.dim() >= 2 and ('conv' in name or 'fc' in name or 'linear' in name
                             or 'weight' in name and p.dim() >= 2):
            saved[name] = p.data.clone()
            noise = 1.0 + sigma * torch.randn(p.shape, generator=gen)
            noise.clamp_(min=0.0)
            p.data.mul_(noise)
    return saved

def restore(net, saved):
    d = dict(net.named_parameters())
    for name, w in saved.items():
        d[name].data.copy_(w)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nets', nargs='+',
                    default=['lenet5_mnist', 'resnet20_mnist',
                             'vgg_cifar10', 'vgg_cifar100'])
    ap.add_argument('--sigmas', nargs='+', type=float,
                    default=[0.0, 0.05, 0.10, 0.15, 0.20])
    ap.add_argument('--trials', type=int, default=3)
    ap.add_argument('--out', default=str(FIG/'rram_variation_accuracy.csv'))
    args = ap.parse_args()

    H, D = hw.load_H()
    Hcal = H.clone(); Hcal[2, 0] = 0.0            # calibrated harmonic term
    hwmodel = hw.HwInject(torch.diag(D) @ Hcal, 1.0)

    rows = []
    for name in args.nets:
        net, ds, convs = hw.build(name)
        loader = torch.utils.data.DataLoader(ds, batch_size=256, shuffle=False,
                                             num_workers=4)
        for combo, inj in [('var_only', None), ('var+hw_cal', hwmodel)]:
            for sig in args.sigmas:
                accs = []
                for t in range(args.trials if sig > 0 else 1):
                    gen = torch.Generator().manual_seed(2026 + t)
                    saved = perturb_weights(net, sig, gen)
                    accs.append(hw.eval_model(net, loader, inj, convs))
                    restore(net, saved)
                m, s = float(np.mean(accs)), float(np.std(accs))
                rows.append([name, combo, f'{sig:.2f}', f'{m:.2f}', f'{s:.2f}'])
                print(f'{name:14s} {combo:10s} sigma={sig:.2f} '
                      f'acc={m:.2f}+-{s:.2f}%', flush=True)
    with open(args.out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['network', 'case', 'sigma', 'accuracy_mean', 'accuracy_std'])
        w.writerows(rows)
    print('wrote', args.out)

if __name__ == '__main__':
    main()
