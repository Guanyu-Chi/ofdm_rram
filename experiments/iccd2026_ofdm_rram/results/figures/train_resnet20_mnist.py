#!/usr/bin/env python3
"""Train ResNet20 (repo's CIFAR-style ResNet, depth=20) on MNIST.

Uses the OFDM_QAM_crossbar resnet.py architecture with the first conv adapted
to 1-channel 28x28 input (avgpool 7), same preprocessing family as the other
checkpoints (Normalize 0.5/0.5). Saves model_best.pth.tar-compatible dict.
"""
import time, sys
from pathlib import Path
import torch, torch.nn as nn
import torchvision, torchvision.transforms as T
from torch.utils.data import DataLoader

BASE = Path('/nas/ei/share/TUEIEDAscratch/ge86duw/OFDM_QAM_crossbar')
OUT = Path(__file__).resolve().parent / 'resnet20_mnist_model_best.pth.tar'

import importlib.util
spec = importlib.util.spec_from_file_location('resnet', BASE/'models/resnet.py')
rmod = importlib.util.module_from_spec(spec); spec.loader.exec_module(rmod)

def build():
    net = rmod.ResNet_cifar10(num_classes=10, depth=20)
    net.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1, bias=False)
    net.avgpool = nn.AvgPool2d(7)
    return net

def main():
    torch.manual_seed(2026)
    torch.set_num_threads(32)
    tf = T.Compose([T.ToTensor(), T.Normalize((0.5,), (0.5,))])
    tr = torchvision.datasets.MNIST(str(BASE/'data/MNIST'), train=True, download=False, transform=tf)
    te = torchvision.datasets.MNIST(str(BASE/'data/MNIST'), train=False, download=False, transform=tf)
    ltr = DataLoader(tr, batch_size=256, shuffle=True, num_workers=8)
    lte = DataLoader(te, batch_size=512, num_workers=4)
    net = build()
    opt = torch.optim.SGD(net.parameters(), lr=0.1, momentum=0.9, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.MultiStepLR(opt, [4, 7], gamma=0.1)
    lossf = nn.CrossEntropyLoss()
    best = 0.0
    for ep in range(9):
        net.train(); t0=time.time()
        for xb, yb in ltr:
            opt.zero_grad(); loss = lossf(net(xb), yb); loss.backward(); opt.step()
        sched.step()
        net.eval(); c=t=0
        with torch.no_grad():
            for xb, yb in lte:
                c += (net(xb).argmax(1)==yb).sum().item(); t += len(yb)
        acc = 100*c/t
        print(f'epoch {ep}: test {acc:.2f}%  ({time.time()-t0:.0f}s)', flush=True)
        if acc > best:
            best = acc
            torch.save({'model':'resnet20_mnist','epoch':ep,'state_dict':net.state_dict(),
                        'best_prec1':best,'config':'1ch conv1, avgpool7, depth20'}, OUT)
    print(f'best {best:.2f}% -> {OUT}')

if __name__ == '__main__':
    main()
