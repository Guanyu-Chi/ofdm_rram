#!/usr/bin/env python3
"""Export and plot the 128 saved bitline waveforms from the Spectre PSF ASCII output."""

from pathlib import Path
import csv
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
WAVE = ROOT / "results" / "sim_run_zerowarn" / "psf" / "tbtran.tran.tran"
OUT_DIR = ROOT / "results" / "sim_run_zerowarn"
CSV_OUT = OUT_DIR / "bl128_waveforms.csv"
PDF_OUT = OUT_DIR / "bl128_waveforms.pdf"
PNG_OUT = OUT_DIR / "bl128_waveforms.png"
SUMMARY_OUT = OUT_DIR / "bl128_waveform_summary.csv"

BL_NAMES = [f"bl{i:03d}" for i in range(128)]
BL_SET = set(BL_NAMES)
DPI = 600
FIGSIZE = (8.2, 4.8)
TEXT = "#1F2933"
GRID = "#D9DEE6"
LINE = "#4C78A8"
HIGHLIGHT = "#F28E2B"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def parse_psf_bl_waveforms():
    rows = []
    current_time = None
    current = {}
    in_value = False

    with WAVE.open() as f:
        for raw in f:
            line = raw.strip()
            if line == "VALUE":
                in_value = True
                continue
            if not in_value or not line.startswith('"'):
                continue

            key_part, value_part = line.rsplit(" ", 1)
            key = key_part.split('"')[1]
            value = float(value_part)

            if key == "time":
                if current_time is not None:
                    rows.append((current_time, current))
                current_time = value
                current = {}
            elif key in BL_SET:
                current[key] = value

    if current_time is not None:
        rows.append((current_time, current))
    return rows


def write_csv(rows):
    with CSV_OUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_s"] + BL_NAMES)
        for t, vals in rows:
            writer.writerow([f"{t:.15e}"] + [f"{vals.get(name, float('nan')):.15e}" for name in BL_NAMES])


def write_summary(rows):
    stats = {name: {"min": float("inf"), "max": float("-inf"), "final": 0.0} for name in BL_NAMES}
    for _t, vals in rows:
        for name in BL_NAMES:
            v = vals[name]
            if v < stats[name]["min"]:
                stats[name]["min"] = v
            if v > stats[name]["max"]:
                stats[name]["max"] = v
            stats[name]["final"] = v

    with SUMMARY_OUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["bitline", "min_v", "max_v", "peak_to_peak_v", "final_v", "current_equivalent_note"])
        for name in BL_NAMES:
            s = stats[name]
            writer.writerow([
                name,
                f"{s['min']:.15e}",
                f"{s['max']:.15e}",
                f"{(s['max'] - s['min']):.15e}",
                f"{s['final']:.15e}",
                "1 ohm BL load: current in A equals voltage in V divided by 1 ohm",
            ])


def plot_waveforms(rows):
    times_ns = [t * 1e9 for t, _vals in rows]
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for idx, name in enumerate(BL_NAMES):
        ys = [vals[name] for _t, vals in rows]
        color = HIGHLIGHT if name in {"bl000", "bl064", "bl127"} else LINE
        alpha = 0.85 if name in {"bl000", "bl064", "bl127"} else 0.16
        lw = 1.3 if name in {"bl000", "bl064", "bl127"} else 0.55
        label = name if name in {"bl000", "bl064", "bl127"} else None
        ax.plot(times_ns, ys, color=color, alpha=alpha, linewidth=lw, label=label)

    ax.set_xlabel("Time (ns)", fontsize=12.5, fontweight="bold", color=TEXT)
    ax.set_ylabel("Bitline voltage (V)", fontsize=12.5, fontweight="bold", color=TEXT)
    ax.set_xlim(min(times_ns), max(times_ns))
    ax.grid(True, color=GRID, linewidth=0.7, alpha=0.8)
    ax.tick_params(axis="both", labelsize=10.5, colors=TEXT)
    for spine in ax.spines.values():
        spine.set_color("#9AA5B1")
        spine.set_linewidth(0.8)

    ax.text(
        0.012, 0.975,
        "128 saved bitline waveforms: bl000-bl127",
        transform=ax.transAxes,
        ha="left", va="top", fontsize=12.3, fontweight="bold", color=TEXT,
    )
    ax.text(
        0.012, 0.92,
        "Spectre transient output, 80 ns read window",
        transform=ax.transAxes,
        ha="left", va="top", fontsize=10.8, color=TEXT,
    )
    ax.legend(loc="upper right", fontsize=9.5, frameon=True)

    fig.savefig(PDF_OUT, bbox_inches="tight", facecolor="white")
    fig.savefig(PNG_OUT, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    rows = parse_psf_bl_waveforms()
    if not rows:
        raise RuntimeError(f"No BL waveform rows parsed from {WAVE}")
    missing = [name for name in BL_NAMES if name not in rows[-1][1]]
    if missing:
        raise RuntimeError(f"Missing BL signals in final timestep: {missing[:5]}")
    write_csv(rows)
    write_summary(rows)
    plot_waveforms(rows)
    print(f"parsed_time_points={len(rows)}")
    print(f"saved_traces={len(BL_NAMES)}")
    print(f"wrote {CSV_OUT}")
    print(f"wrote {SUMMARY_OUT}")
    print(f"wrote {PDF_OUT}")
    print(f"wrote {PNG_OUT}")


if __name__ == "__main__":
    main()
