#!/usr/bin/env python3
"""Level-3 hardware-aware mapping: minimal trained linear layer on MNIST.

Trains a 784->10 softmax linear classifier (numpy), quantizes to the paper's
signal representation (binary +-1 weights via differential columns, 2-bit
inputs), then injects the measured v5 peripheral model:
  y_hw = C * (H @ y_ideal_group)   per 4-carrier group
with H the measured end-to-end channel matrix (Gilbert |z|, columns
normalized to own diagonal), and C the measured four-tone compression factor.
First-order empirical model; magnitudes only (worst-case additive leakage).
"""
import csv, gzip, struct
from pathlib import Path
import numpy as np

RAW = Path('/nas/ei/share/TUEIEDAscratch/ge86duw/ICCD/datasets/mnist/MNIST/raw')

def idx(path):
    d = open(path,'rb').read()
    magic, = struct.unpack('>I', d[:4])
    if magic == 2051:
        n,r,c = struct.unpack('>III', d[4:16])
        return np.frombuffer(d,np.uint8,offset=16).reshape(n,r*c)/255.0
    n, = struct.unpack('>I', d[4:8])
    return np.frombuffer(d,np.uint8,offset=8)

xtr, ytr = idx(RAW/'train-images-idx3-ubyte'), idx(RAW/'train-labels-idx1-ubyte')
xte, yte = idx(RAW/'t10k-images-idx3-ubyte'), idx(RAW/'t10k-labels-idx1-ubyte')
rng = np.random.default_rng(2026)

# --- train float softmax layer ---
W = np.zeros((784,10)); b = np.zeros(10)
for ep in range(6):
    perm = rng.permutation(len(xtr))
    for i in range(0, len(xtr), 256):
        bx, by = xtr[perm[i:i+256]], ytr[perm[i:i+256]]
        z = bx@W + b
        z -= z.max(1, keepdims=True)
        p = np.exp(z); p /= p.sum(1, keepdims=True)
        p[np.arange(len(by)), by] -= 1
        W -= 0.05*(bx.T@p)/len(by); b -= 0.05*p.mean(0)*len(by)/len(by)
def acc(logits, y): return float((logits.argmax(1)==y).mean())
base = acc(xte@W+b, yte)

# --- quantize: binary weights (sign, per-neuron scale), 2-bit inputs ---
alpha = np.abs(W).mean(0)
Wb = np.sign(W)*alpha
xq = np.round(np.clip(xte,0,1)*3)/3.0
ideal_logits = xq@Wb + b
ideal = acc(ideal_logits, yte)

# --- hardware model from v5 measurements ---
gil = {}
for r in csv.DictReader(open('figures/gilbert_c1_metrics_v5.csv')):
    gil[(r['stim'], r['channel'])] = float(r['mag_v'])
chs = ['250','500','750','1g']
H = np.array([[gil[(j,k)]/gil[(j,j)] for j in chs] for k in chs])  # H[k,j]
C = 0.47  # measured four-tone compression (0.42-0.48)
slot_gain = C * H.sum(0)          # digital sum folds H columns: 1^T H y
gain_vec = np.tile(slot_gain, 784//4)
hw_logits = (xq*gain_vec)@Wb + b
hw = acc(hw_logits, yte)

# layer-level fidelity on 1000-sample subset
sub = slice(0,1000)
zi, zh = ideal_logits[sub], hw_logits[sub]
cos = float(np.mean(np.sum(zi*zh,1)/(np.linalg.norm(zi,axis=1)*np.linalg.norm(zh,axis=1)+1e-12)))
nerr = float(np.linalg.norm(zh-zi)/np.linalg.norm(zi))
cons = float((zi.argmax(1)==zh.argmax(1)).mean())

rows=[['metric','value','note'],
 ['float_baseline_acc', f'{base:.4f}', '784->10 softmax, full MNIST test set'],
 ['ideal_mapped_acc', f'{ideal:.4f}', 'binary +-1 weights, 2-bit inputs'],
 ['hw_aware_mapped_acc', f'{hw:.4f}', 'v5 H (end-to-end), C=0.47'],
 ['acc_degradation_vs_ideal', f'{ideal-hw:.4f}', ''],
 ['cosine_similarity_subset1000', f'{cos:.5f}', 'pre-activation ideal vs hw'],
 ['normalized_error_subset1000', f'{nerr:.4f}', 'L2'],
 ['classification_consistency_subset1000', f'{cons:.4f}', 'same argmax'],
 ['slot_gains', ' '.join(f'{g:.4f}' for g in slot_gain), 'C*colsum(H) per carrier slot']]
with open('figures/mapped_layer_hw_eval.csv','w',newline='') as f:
    csv.writer(f).writerows(rows)
for r in rows[1:]: print(f'{r[0]:38s} {r[1]}  {r[2]}')
np.savetxt('figures/mapped_layer_H_matrix.csv', H, delimiter=',', fmt='%.5f',
           header='end-to-end channel matrix H[k,j]=|z_k(stim j)|/|z_j(stim j)|, rows/cols=250,500,750,1000MHz')
