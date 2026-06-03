#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SIZE="${1:-8}"
NETLIST="$ROOT/tb/tb_ofdm_qam_${SIZE}x${SIZE}_sanity.scs"
OUTDIR="$ROOT/results/sanity_${SIZE}x${SIZE}"

mkdir -p "$OUTDIR"

if ! command -v spectre >/dev/null 2>&1; then
  echo "Circuit simulator executable not found in PATH." >&2
  exit 127
fi

spectre "$NETLIST" +escchars +log "$OUTDIR/run.log" -format psfascii -raw "$OUTDIR/psf"
