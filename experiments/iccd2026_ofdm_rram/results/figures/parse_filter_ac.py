#!/usr/bin/env python3
"""Parse Spectre AC nutascii: rows are pointindex + complex values."""
import numpy as np, re, sys

def read_ac(path):
    names=[]; toks=[]; invals=False
    for ln in open(path, errors='ignore'):
        if ln.startswith('Variables:'):
            t=ln.split()
            if len(t)>=3: names.append(t[2])
            continue
        if ln.startswith('Values:'): invals=True; continue
        if not invals:
            m=re.match(r'\s*(\d+)\s+(\S+)\s+\S+', ln)
            if m and names: names.append(m.group(2))
            continue
        toks.extend(ln.split())
    vals=[]
    for tok in toks:
        if ',' in tok:
            r,i=tok.split(','); vals.append(complex(float(r),float(i)))
        else:
            vals.append(complex(float(tok),0))
    n=len(names)+1  # leading point index
    a=np.array(vals[:(len(vals)//n)*n]).reshape(-1,n)[:,1:]
    return names, a

if __name__=='__main__':
    names,a=read_ac(sys.argv[1])
    idx={nm:i for i,nm in enumerate(names)}
    f=a[:,idx['freq']].real
    carriers={'250':250e6,'500':500e6,'750':750e6,'1g':1000e6}
    H={c:np.abs(a[:,idx[f'bf{c}p']]-a[:,idx[f'bf{c}n']]) for c in carriers}
    for c,fc in carriers.items():
        k=np.argmin(abs(f-fc)); own=H[c][k]
        wv,wc=max((H[c][np.argmin(abs(f-fo))],lc) for lc,fo in carriers.items() if lc!=c)
        kp=np.argmax(H[c])
        print(f'ch{c}: peak@{f[kp]/1e6:.0f}MHz={H[c][kp]:.4g}  @own({fc/1e6:.0f})={own:.4g}  worst@other={wv:.4g}({wc})  ratio={own/wv:.1f}x')
