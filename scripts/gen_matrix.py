#!/usr/bin/env python3
"""Generate the programmed binary conductance matrix for read-state validation."""

from pathlib import Path
import csv
import random

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "config" / "G_matrix_seed2026.csv"

ROWS = 128
COLS = 128
SEED = 2026
RON = 1_000.0
ROFF = 1_000_000.0
G_ON = 1.0 / RON
G_OFF = 1.0 / ROFF


def main() -> None:
    rng = random.Random(SEED)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    on_count = 0
    with OUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["row", "col", "state", "conductance_s"])
        for r in range(ROWS):
            for c in range(COLS):
                state = "Ron" if rng.random() < 0.5 else "Roff"
                if state == "Ron":
                    on_count += 1
                writer.writerow([r, c, state, f"{G_ON if state == 'Ron' else G_OFF:.12e}"])
    print(f"wrote {OUT}")
    print(f"rows={ROWS} cols={COLS} cells={ROWS * COLS} ron_cells={on_count} roff_cells={ROWS * COLS - on_count}")


if __name__ == "__main__":
    main()
