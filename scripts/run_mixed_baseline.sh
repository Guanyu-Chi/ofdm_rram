#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NETLIST="$ROOT/tb/tb_conventional_mixed_16qam_128x128.scs"
OUTDIR="$ROOT/results/mixed_baseline"

mkdir -p "$OUTDIR"

if ! command -v spectre >/dev/null 2>&1; then
  echo "Circuit simulator executable not found in PATH." >&2
  exit 127
fi

spectre "$NETLIST" +escchars +log "$OUTDIR/run.log" -format psfascii -raw "$OUTDIR/psf"
