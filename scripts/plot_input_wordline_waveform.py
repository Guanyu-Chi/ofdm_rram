#!/usr/bin/env python3
"""Plot generated OFDM wordline input carriers and composite PWL waveform."""

from pathlib import Path
import math
import re
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
NETLIST = ROOT / "netlist" / "clean_128x128_crossbar.scs"
OUT_DIR = ROOT / "review_package"
OUT_STEM = "input_wordline_four_carriers_wl000"
NODE = "VWL000"
ROW = 0
STOP = 80e-9
DT = 0.125e-9
CARRIERS = [250e6, 500e6, 750e6, 1e9]
LEVELS = [-0.3, -0.1, 0.3, 0.1]

FIGSIZE = (7.2, 4.8)
DPI = 600
COLORS = ["#4C78A8", "#72B7B2", "#59A14F", "#F28E2B"]
COMPOSITE_COLOR = "#1F2933"
TEXT = "#1F2933"
GRID = "#D9DEE6"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def carrier_components(row: int):
    comps = []
    for k, freq in enumerate(CARRIERS):
        i_level = LEVELS[(row + 2 * k) % len(LEVELS)]
        q_level = LEVELS[(row + 2 * k + 1) % len(LEVELS)]
        comps.append((i_level, q_level, freq))
    return comps


def extract_pwl(node: str):
    text = NETLIST.read_text()
    pattern = re.compile(r"^" + re.escape(node) + r"\s+.*?wave=\[([^\]]+)\]", re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"Cannot find PWL source {node} in {NETLIST}")
    values = [float(x) for x in match.group(1).split()]
    return values[0::2], values[1::2]


def main():
    t, composite_from_netlist = extract_pwl(NODE)
    t_ns = [x * 1e9 for x in t]
    comps = carrier_components(ROW)
    component_waves = []
    for i_level, q_level, freq in comps:
        component_waves.append([
            i_level * math.cos(2 * math.pi * freq * tt)
            + q_level * math.sin(2 * math.pi * freq * tt)
            for tt in t
        ])

    fig, axes = plt.subplots(5, 1, figsize=FIGSIZE, sharex=True)
    fig.patch.set_facecolor("white")

    for idx, ax in enumerate(axes[:4]):
        i_level, q_level, freq = comps[idx]
        ax.plot(t_ns, component_waves[idx], color=COLORS[idx], linewidth=1.3)
        ax.text(
            0.012, 0.82,
            f"Carrier {idx + 1}: {freq/1e6:.0f} MHz, I={i_level:.1f} V, Q={q_level:.1f} V",
            transform=ax.transAxes,
            ha="left", va="top",
            fontsize=10.5, fontweight="bold", color=TEXT,
        )
        ax.set_ylabel("V", fontsize=10.5, fontweight="bold", color=TEXT)

    axes[4].plot(t_ns, composite_from_netlist, color=COMPOSITE_COLOR, linewidth=1.4)
    axes[4].text(
        0.012, 0.82,
        "Composite WL000 PWL input",
        transform=axes[4].transAxes,
        ha="left", va="top",
        fontsize=10.5, fontweight="bold", color=TEXT,
    )
    axes[4].set_ylabel("V", fontsize=10.5, fontweight="bold", color=TEXT)
    axes[4].set_xlabel("Time (ns)", fontsize=12.0, fontweight="bold", color=TEXT)

    for ax in axes:
        ax.set_facecolor("white")
        ax.grid(True, color=GRID, linewidth=0.6, alpha=0.8)
        ax.tick_params(axis="both", labelsize=9.5, colors=TEXT)
        ax.set_xlim(0, 16)
        vmax = max(abs(y) for line in ax.lines for y in line.get_ydata())
        ax.set_ylim(-1.18 * vmax, 1.18 * vmax)
        for spine in ax.spines.values():
            spine.set_color("#9AA5B1")
            spine.set_linewidth(0.8)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf = OUT_DIR / f"{OUT_STEM}.pdf"
    png = OUT_DIR / f"{OUT_STEM}.png"
    fig.savefig(pdf, bbox_inches="tight", facecolor="white")
    fig.savefig(png, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {pdf}")
    print(f"wrote {png}")
    print(f"points={len(t)} shown_window=0-16ns full_window=80ns")


if __name__ == "__main__":
    main()
