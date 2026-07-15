#!/usr/bin/env python3
"""Generate matched conventional mixed 16-QAM baseline testbench."""

from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
CARRIERS = [250e6, 500e6, 750e6, 1e9]
PHASE_BINS = 16
COLS = 128


def main() -> None:
    out = ROOT / "tb" / "tb_conventional_mixed_16qam_128x128.scs"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        f.write("// Matched conventional mixed 16-QAM read-path baseline testbench\n")
        f.write("// Same crossbar, carriers, BPFs, phase-window verification demodulator, and integration window.\n")
        f.write("simulator lang=spectre\n")
        f.write('include "../netlist/clean_128x128_crossbar.scs"\n\n')
        f.write("parameters rclosed_mix=1 ropen_mix=1G\n\n")
        for idx, freq in enumerate(CARRIERS):
            period = 1.0 / freq
            width = period / PHASE_BINS
            f.write(f"VREFI_{idx} (conv_ref_i_{idx} 0) vsource type=sine freq={freq:.0f} ampl=1 phase=90\n")
            f.write(f"VREFQ_{idx} (conv_ref_q_{idx} 0) vsource type=sine freq={freq:.0f} ampl=1 phase=0\n")
            f.write(f"RREFI_{idx} (conv_ref_i_{idx} 0) resistor r=1G\n")
            f.write(f"RREFQ_{idx} (conv_ref_q_{idx} 0) resistor r=1G\n")
            for b in range(PHASE_BINS):
                delay = b * width
                f.write(
                    f"VCONVWIN_{idx}_{b:02d} (conv_win_{idx}_{b:02d} 0) vsource type=pulse "
                    f"val0=-1 val1=1 period={period:.12e} width={width:.12e} "
                    f"delay={delay:.12e} rise=1p fall=1p\n"
                )
            f.write("\n")
        for col in range(COLS):
            for idx, freq in enumerate(CARRIERS):
                lref = 1e-6
                cval = 1.0 / ((2 * math.pi * freq) ** 2 * lref)
                rval = 2 * math.pi * freq * lref / 20.0
                f.write(f"// conventional mixed baseline bl{col:03d}, carrier_{idx}: {freq:.0f} Hz\n")
                f.write(f"CCONVBPF_c{col:03d}_{idx} (bl{col:03d} n_conv_cbpf_c{col:03d}_{idx}) capacitor c={cval:.12e}\n")
                f.write(f"LCONVBPF_c{col:03d}_{idx} (n_conv_cbpf_c{col:03d}_{idx} conv_bpf_c{col:03d}_{idx}) inductor l={lref:.12e}\n")
                f.write(f"RCONVBPF_c{col:03d}_{idx} (conv_bpf_c{col:03d}_{idx} 0) resistor r={rval:.12e}\n")
                for b in range(PHASE_BINS):
                    phase = 2 * math.pi * (b + 0.5) / PHASE_BINS
                    igain = math.cos(phase)
                    qgain = math.sin(phase)
                    f.write(f"ECONVI_c{col:03d}_{idx}_{b:02d} (conv_i_src_c{col:03d}_{idx}_{b:02d} 0 conv_bpf_c{col:03d}_{idx} 0) vcvs gain={igain:.12e}\n")
                    f.write(f"SCONVI_c{col:03d}_{idx}_{b:02d} (conv_i_src_c{col:03d}_{idx}_{b:02d} conv_i_c{col:03d}_{idx} conv_win_{idx}_{b:02d} 0) relay vt1=-1m vt2=1m ropen=ropen_mix rclosed=rclosed_mix\n")
                    f.write(f"ECONVQ_c{col:03d}_{idx}_{b:02d} (conv_q_src_c{col:03d}_{idx}_{b:02d} 0 conv_bpf_c{col:03d}_{idx} 0) vcvs gain={qgain:.12e}\n")
                    f.write(f"SCONVQ_c{col:03d}_{idx}_{b:02d} (conv_q_src_c{col:03d}_{idx}_{b:02d} conv_q_c{col:03d}_{idx} conv_win_{idx}_{b:02d} 0) relay vt1=-1m vt2=1m ropen=ropen_mix rclosed=rclosed_mix\n")
                f.write(f"RCONVI_c{col:03d}_{idx} (conv_i_c{col:03d}_{idx} 0) resistor r=1G\n")
                f.write(f"RCONVQ_c{col:03d}_{idx} (conv_q_c{col:03d}_{idx} 0) resistor r=1G\n")
                f.write(f"RCONVINTI_c{col:03d}_{idx} (conv_i_c{col:03d}_{idx} ConvIcar_c{col:03d}_{idx}) resistor r=1k\n")
                f.write(f"CCONVINTI_c{col:03d}_{idx} (ConvIcar_c{col:03d}_{idx} 0) capacitor c=80p\n")
                f.write(f"RCONVINTQ_c{col:03d}_{idx} (conv_q_c{col:03d}_{idx} ConvQcar_c{col:03d}_{idx}) resistor r=1k\n")
                f.write(f"CCONVINTQ_c{col:03d}_{idx} (ConvQcar_c{col:03d}_{idx} 0) capacitor c=80p\n")
                f.write(f"save conv_bpf_c{col:03d}_{idx} ConvIcar_c{col:03d}_{idx} ConvQcar_c{col:03d}_{idx}\n\n")
        f.write("tbtran tran stop=80n maxstep=5p\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
