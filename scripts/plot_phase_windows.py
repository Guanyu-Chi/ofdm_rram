#!/usr/bin/env python3
"""Plot phase-window control pulses used by the verification demodulator."""

from pathlib import Path
import re
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TB = ROOT / "tb" / "tb_ofdm_qam_128x128_zerowarn.scs"
OUT_DIR = ROOT / "review_package"
OUT_STEM = "phase_window_waveforms_carrier0"
CARRIER = 0
NUM_WINDOWS = 16
SAMPLES = 1601

FIGSIZE = (7.2, 5.2)
DPI = 600
TEXT = "#1F2933"
GRID = "#D9DEE6"
COLORS = [
    "#4C78A8", "#72B7B2", "#59A14F", "#F28E2B",
    "#8E6C8A", "#6B8E23", "#7A8FA6", "#B07AA1",
]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def parse_value(token: str) -> float:
    token = token.strip()
    suffix = token[-1].lower()
    scales = {"p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3, "k": 1e3, "g": 1e9}
    if suffix in scales:
        return float(token[:-1]) * scales[suffix]
    return float(token)


def parse_vwin(idx: int):
    text = TB.read_text()
    name = f"VWIN_{CARRIER}_{idx:02d}"
    pattern = re.compile(
        rf"^{name} \(win_{CARRIER}_{idx:02d} 0\) vsource type=pulse "
        rf"val0=([^ ]+) val1=([^ ]+) period=([^ ]+) width=([^ ]+) delay=([^ ]+) rise=([^ ]+) fall=([^\n]+)",
        re.MULTILINE,
    )
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"Cannot find {name} in {TB}")
    val0, val1, period, width, delay, rise, fall = [parse_value(x) for x in match.groups()]
    return {
        "name": name,
        "node": f"win_{CARRIER}_{idx:02d}",
        "val0": val0,
        "val1": val1,
        "period": period,
        "width": width,
        "delay": delay,
        "rise": rise,
        "fall": fall,
    }


def pulse_value(t, spec):
    period = spec["period"]
    width = spec["width"]
    delay = spec["delay"]
    val0 = spec["val0"]
    val1 = spec["val1"]
    rise = spec["rise"]
    fall = spec["fall"]
    tau = (t - delay) % period
    # Before first delayed pulse, stay at val0.
    before_first = t < delay
    y = np.full_like(t, val0, dtype=float)
    active = ~before_first
    ta = tau[active]
    ya = np.full_like(ta, val0, dtype=float)
    rising = ta < rise
    high = (ta >= rise) & (ta < width)
    falling = (ta >= width) & (ta < width + fall)
    ya[rising] = val0 + (val1 - val0) * ta[rising] / rise
    ya[high] = val1
    ya[falling] = val1 + (val0 - val1) * (ta[falling] - width) / fall
    y[active] = ya
    return y


def main():
    specs = [parse_vwin(i) for i in range(NUM_WINDOWS)]
    period = specs[0]["period"]
    t = np.linspace(0, period, SAMPLES)
    t_ns = t * 1e9

    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    offsets = np.arange(NUM_WINDOWS)[::-1] * 2.35
    for i, spec in enumerate(specs):
        y = pulse_value(t, spec)
        ax.plot(t_ns, y + offsets[i], color=COLORS[i % len(COLORS)], linewidth=1.1)
        ax.text(
            -0.05, offsets[i], spec["node"],
            ha="right", va="center", fontsize=8.8, fontweight="bold", color=TEXT,
        )

    ax.set_xlabel("Time (ns)", fontsize=12.0, fontweight="bold", color=TEXT)
    ax.set_ylabel("Window pulse nodes", fontsize=12.0, fontweight="bold", color=TEXT)
    ax.set_xlim(-0.18, period * 1e9)
    ax.set_yticks([])
    ax.grid(True, axis="x", color=GRID, linewidth=0.7, alpha=0.8)
    ax.tick_params(axis="x", labelsize=10.5, colors=TEXT)
    for spine in ax.spines.values():
        spine.set_color("#9AA5B1")
        spine.set_linewidth(0.8)

    ax.text(
        0.012, 0.985,
        "Carrier 0 phase-window pulses: win_0_00 to win_0_15",
        transform=ax.transAxes,
        ha="left", va="top", fontsize=12.0, fontweight="bold", color=TEXT,
    )
    ax.text(
        0.012, 0.94,
        "Period = 4 ns, width = 0.25 ns, val0 = -1 V, val1 = 1 V",
        transform=ax.transAxes,
        ha="left", va="top", fontsize=10.5, color=TEXT,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf = OUT_DIR / f"{OUT_STEM}.pdf"
    png = OUT_DIR / f"{OUT_STEM}.png"
    fig.savefig(pdf, bbox_inches="tight", facecolor="white")
    fig.savefig(png, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    csv = OUT_DIR / f"{OUT_STEM}.csv"
    with csv.open("w") as f:
        f.write("node,val0_v,val1_v,period_s,width_s,delay_s,rise_s,fall_s\n")
        for spec in specs:
            f.write(
                f"{spec['node']},{spec['val0']},{spec['val1']},{spec['period']},"
                f"{spec['width']},{spec['delay']},{spec['rise']},{spec['fall']}\n"
            )

    print(f"wrote {pdf}")
    print(f"wrote {png}")
    print(f"wrote {csv}")


if __name__ == "__main__":
    main()
