#!/usr/bin/env python3
"""Hardware-aware inference evaluation on real trained networks.

Loads the existing trained checkpoints (LeNet5-MNIST, VGG8-CIFAR10,
VGG8-CIFAR100) from OFDM_QAM_crossbar/results and evaluates the full test
sets under the measured v5 peripheral hardware model, following the same
batch-dimension carrier-multiplexing protocol as the project's
*_with_mismatch_carrier_v2 models (consecutive batch samples ride different
carrier branches; injection after every conv layer, pre-BN).

Injected model (per group of 4 batch samples = carriers 250/500/750/1000 MHz):
    y_hw = C * (H @ y_ideal)
with H the measured end-to-end channel matrix (Gilbert path, columns
normalized to their own diagonal; includes the harmonic-limited ch3 leakage)
and C = 0.47 the measured four-tone compression. Cases:
  baseline   : no injection (checkpoint accuracy reproduction)
  crosstalk  : H only (single-tone-amplitude regime)
  hw_full    : C*H (simultaneous four-carrier regime)
"""
import argparse, csv, sys, time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as T

BASE = Path('/nas/ei/share/TUEIEDAscratch/ge86duw/OFDM_QAM_crossbar')
FIG = Path(__file__).resolve().parent

def load_module(fname):
    import importlib.util
    spec = importlib.util.spec_from_file_location(fname, BASE/'models'/f'{fname}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def load_H():
    rows = {}
    with open(FIG / 'gilbert_c1_metrics_v5.csv') as f:
        for r in csv.DictReader(f):
            rows[(r['stim'], r['channel'])] = float(r['mag_v'])
    chs = ['250', '500', '750', '1g']
    H = np.array([[rows[(j, k)] / rows[(j, j)] for j in chs] for k in chs])
    # per-channel four-tone gain imbalance, common-mode compression removed
    # (the common gain is calibrated at the readout; the residual is the
    #  measured per-channel deviation of fourtone/single ratios)
    imb = []
    with open(FIG / 'gilbert_channel_margin_v5.csv') as f:
        for r in csv.DictReader(f):
            imb.append(float(r['fourtone_over_single']))
    D = np.array(imb) / np.mean(imb)
    return torch.tensor(H, dtype=torch.float32), torch.tensor(D, dtype=torch.float32)

class HwInject:
    def __init__(self, H, C):
        self.M = C * H  # 4x4
    def __call__(self, x):
        n = (x.shape[0] // 4) * 4
        if n == 0:
            return x
        head = x[:n].reshape(n // 4, 4, -1)
        mixed = torch.einsum('kj,gjf->gkf', self.M.to(x.dtype), head)
        out = x.clone()
        out[:n] = mixed.reshape(n, *x.shape[1:])
        return out

def eval_model(net, loader, inject, conv_names):
    hooks = []
    if inject is not None:
        for name, mod in net.named_modules():
            if name in conv_names:
                hooks.append(mod.register_forward_hook(
                    lambda m, i, o: inject(o)))
    net.eval()
    correct = total = 0
    with torch.no_grad():
        for xb, yb in loader:
            out = net(xb)
            correct += (out.argmax(1) == yb).sum().item()
            total += len(yb)
    for h in hooks:
        h.remove()
    return 100.0 * correct / total

def build(name):
    if name == 'resnet20_mnist':
        import torch.nn as nn
        rmod = load_module('resnet')
        net = rmod.ResNet_cifar10(num_classes=10, depth=20)
        net.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1, bias=False)
        net.avgpool = nn.AvgPool2d(7)
        tf = T.Compose([T.ToTensor(), T.Normalize((0.5,), (0.5,))])
        ds = torchvision.datasets.MNIST(str(BASE/'data/MNIST'), train=False,
                                        download=False, transform=tf)
        convs = [n for n, m in net.named_modules()
                 if isinstance(m, nn.Conv2d) and 'downsample' not in n]
        ck = torch.load(FIG/'resnet20_mnist_model_best.pth.tar',
                        map_location='cpu', weights_only=False)
        net.load_state_dict(ck['state_dict'])
        print(f'{name}: checkpoint epoch={ck.get("epoch")} best={ck.get("best_prec1"):.2f}')
        return net, ds, convs
    if name == 'lenet5_mnist':
        net = load_module('lenet5').lenet5(num_classes=10)
        tf = T.Compose([T.Resize(32), T.CenterCrop(28), T.ToTensor(), T.Normalize((0.5,), (0.5,))])
        ds = torchvision.datasets.MNIST(str(BASE/'data/MNIST'), train=False,
                                        download=False, transform=tf)
        convs = ['conv1', 'conv2']
    elif name in ('vgg_cifar10', 'vgg_cifar100'):
        ncls = 10 if name.endswith('10') else 100
        net = load_module('vgg_cifar10').vgg_cifar10(num_classes=ncls)
        tf = T.Compose([T.Resize(32), T.CenterCrop(32), T.ToTensor(),
                        T.Normalize((0.485, 0.456, 0.406),
                                    (0.229, 0.224, 0.225))])
        cls = (torchvision.datasets.CIFAR10 if ncls == 10
               else torchvision.datasets.CIFAR100)
        sub = 'CIFAR10' if ncls == 10 else 'CIFAR100'
        ds = cls(str(BASE/f'data/{sub}'), train=False, download=False,
                 transform=tf)
        convs = [f'conv{i}' for i in range(1, 7)]
    else:
        raise SystemExit(f'unknown {name}')
    ck = torch.load(BASE/f'results/{name}/model_best.pth.tar',
                    map_location='cpu', weights_only=False)
    net.load_state_dict(ck['state_dict'])
    print(f'{name}: checkpoint epoch={ck.get("epoch")} best={ck.get("best_prec1"):.2f}')
    return net, ds, convs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nets', nargs='+',
                    default=['lenet5_mnist', 'resnet20_mnist', 'vgg_cifar10', 'vgg_cifar100'])
    ap.add_argument('--batch', type=int, default=256)
    ap.add_argument('--C', type=float, default=0.47)
    ap.add_argument('--out', default=str(FIG/'hw_aware_network_accuracy.csv'))
    args = ap.parse_args()
    torch.manual_seed(2026)
    H, D = load_H()
    Hcal = H.clone(); Hcal[2, 0] = 0.0  # remove deterministic 250->750 harmonic term
    cases = [('baseline', None),
             ('hw_full_DH', HwInject(torch.diag(D) @ H, 1.0)),
             ('hw_cal_harmonic', HwInject(torch.diag(D) @ Hcal, 1.0))]
    rows = []
    for name in args.nets:
        net, ds, convs = build(name)
        loader = DataLoader(ds, batch_size=args.batch, shuffle=False,
                            num_workers=4)
        for cname, inj in cases:
            t0 = time.time()
            acc = eval_model(net, loader, inj, convs)
            dt = time.time() - t0
            rows.append([name, cname, f'{acc:.2f}', len(ds), f'{dt:.0f}'])
            print(f'  {name:14s} {cname:12s} acc={acc:.2f}%  ({dt:.0f}s)')
    with open(args.out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['network', 'case', 'accuracy_percent', 'test_samples',
                    'eval_seconds'])
        w.writerows(rows)
    print('wrote', args.out)

if __name__ == '__main__':
    main()
