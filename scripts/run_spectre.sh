#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NETLIST="$ROOT/tb/tb_ofdm_qam_128x128.scs"
OUTDIR="$ROOT/results/sim_run"

mkdir -p "$OUTDIR"

if ! command -v spectre >/dev/null 2>&1; then
  echo "Circuit simulator executable not found in PATH." >&2
  echo "No waveform result is generated. Configure the simulator environment and rerun." >&2
  exit 127
fi

spectre "$NETLIST" +escchars +log "$OUTDIR/run.log" -format psfascii -raw "$OUTDIR/psf"
