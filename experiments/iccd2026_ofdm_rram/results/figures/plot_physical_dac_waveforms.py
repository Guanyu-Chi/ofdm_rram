#!/usr/bin/env python3
"""Plot reproducible physical four-code DAC transient waveforms."""
from pathlib import Path
import re
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "results/dac2_fourcode_w450_ascii"
OUT = Path(__file__).resolve().parent / "physical_dac_fourcode_waveforms"

def load_nutaascii(path):
    lines = path.read_text().splitlines()
    names = []
    for line in lines:
        match = re.match(r"\s*\d+\s+(\S+)\s+V\s", line)
        if match:
            names.append(match.group(1))
        if line == "Values:":
            break
    start = lines.index("Values:") + 1
    rows, index, width = [], start, len(names) + 1
    while index < len(lines):
        fields = lines[index].split()
        if len(fields) >= 3 and fields[0].isdigit():
            values = [float(value) for value in fields[1:]]
            index += 1
            while len(values) < width and index < len(lines):
                values += [float(value) for value in lines[index].split()]
                index += 1
            rows.append(values)
        else:
            index += 1
    data = np.asarray(rows)
    return data[:, 0], {name: data[:, pos + 1] for pos, name in enumerate(names)}

time, node = load_nutaascii(RAW)
time_ns = time * 1e9
mask = time_ns <= 64
fig, axes = plt.subplots(4, 1, figsize=(7.0, 5.2), sharex=True,
                         gridspec_kw={"hspace": 0.13})
colors = {"blue": "#1261A0", "orange": "#C65D00", "gray": "#555555", "green": "#2A7F62"}
axes[0].step(time_ns[mask], node["db2501"][mask], where="post", color=colors["blue"], label="MSB")
axes[0].step(time_ns[mask], node["db2500"][mask], where="post", color=colors["orange"], label="LSB")
axes[0].set_ylabel("Code input (V)"); axes[0].legend(ncol=2, frameon=False, loc="upper right")
axes[1].plot(time_ns[mask], node["bl"][mask], color=colors["blue"], lw=0.8)
axes[1].set_ylabel("Bitline (V)")
axes[2].plot(time_ns[mask], node["tiaout"][mask] * 1e3, color=colors["orange"], lw=0.9)
axes[2].set_ylabel("TIA out (mV)")
axes[3].plot(time_ns[mask], (node["di250t"] - node["di250c"])[mask] * 1e3, color=colors["green"], lw=0.9, label="I")
axes[3].plot(time_ns[mask], (node["dq250t"] - node["dq250c"])[mask] * 1e3, color=colors["gray"], lw=0.9, label="Q")
axes[3].set_ylabel("Integrated (mV)"); axes[3].set_xlabel("Time (ns)")
axes[3].legend(ncol=2, frameon=False, loc="upper right")
for axis in axes:
    axis.grid(alpha=0.25, lw=0.4)
    for boundary, label in zip([16, 32, 48], ["01", "10", "11"]):
        axis.axvline(boundary, color="#999999", lw=0.55, ls="--")
axes[0].text(7, 0.14, "00", ha="center")
for x, label in zip([24, 40, 56], ["01", "10", "11"]): axes[0].text(x, 0.14, label, ha="center")
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT.with_suffix(".png"), dpi=600, bbox_inches="tight")
fig.savefig(OUT.with_suffix(".pdf"), bbox_inches="tight")
