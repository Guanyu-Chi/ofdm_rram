#!/usr/bin/env python3
"""Generate coherent-demodulation testbenches for every carrier and bit line."""

from pathlib import Path
import argparse
import math

ROOT = Path(__file__).resolve().parents[1]
CARRIERS = [250e6, 500e6, 750e6, 1e9]
PHASE_BINS = 16


def pulse_width(freq: float) -> float:
    return 1.0 / freq / PHASE_BINS


def write_tb(size: int, final: bool = False) -> Path:
    if final:
        out = ROOT / "tb" / "tb_ofdm_qam_128x128.scs"
        include = "../netlist/clean_128x128_crossbar.scs"
        maxstep = "5p"
    else:
        out = ROOT / "tb" / f"tb_ofdm_qam_{size}x{size}_sanity.scs"
        include = f"../netlist/clean_{size}x{size}_crossbar_sanity.scs"
        maxstep = "10p"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        f.write(f"// Coherent-demodulation testbench for {size}x{size} OFDM/QAM-RRAM MVM\n")
        f.write("// Every BL/carrier path uses BPF, phase-window verification demodulator, and RC integration.\n")
        f.write("simulator lang=spectre\n")
        f.write(f"include \"{include}\"\n\n")
        f.write("parameters rclosed_mix=1 ropen_mix=1G\n\n")
        for idx, freq in enumerate(CARRIERS):
            period = 1.0 / freq
            width = pulse_width(freq)
            f.write(f"VREFI_{idx} (ref_i_{idx} 0) vsource type=sine freq={freq:.0f} ampl=1 phase=90\n")
            f.write(f"VREFQ_{idx} (ref_q_{idx} 0) vsource type=sine freq={freq:.0f} ampl=1 phase=0\n")
            f.write(f"RREFI_{idx} (ref_i_{idx} 0) resistor r=1G\n")
            f.write(f"RREFQ_{idx} (ref_q_{idx} 0) resistor r=1G\n")
            for b in range(PHASE_BINS):
                delay = b * width
                f.write(
                    f"VWIN_{idx}_{b:02d} (win_{idx}_{b:02d} 0) vsource type=pulse "
                    f"val0=-1 val1=1 period={period:.12e} width={width:.12e} "
                    f"delay={delay:.12e} rise=1p fall=1p\n"
                )
            f.write("\n")
        for col in range(size):
            for idx, freq in enumerate(CARRIERS):
                lref = 1e-6
                cval = 1.0 / ((2 * math.pi * freq) ** 2 * lref)
                rval = 2 * math.pi * freq * lref / 20.0
                f.write(f"// bl{col:03d}, carrier_{idx}: {freq:.0f} Hz coherent I/Q phase-window verification-demod path\n")
                f.write(f"CBPF_c{col:03d}_{idx} (bl{col:03d} n_cbpf_c{col:03d}_{idx}) capacitor c={cval:.12e}\n")
                f.write(f"LBPF_c{col:03d}_{idx} (n_cbpf_c{col:03d}_{idx} bpf_c{col:03d}_{idx}) inductor l={lref:.12e}\n")
                f.write(f"RBPF_c{col:03d}_{idx} (bpf_c{col:03d}_{idx} 0) resistor r={rval:.12e}\n")
                for b in range(PHASE_BINS):
                    phase = 2 * math.pi * (b + 0.5) / PHASE_BINS
                    igain = math.cos(phase)
                    qgain = math.sin(phase)
                    f.write(f"EMIXI_c{col:03d}_{idx}_{b:02d} (mix_i_src_c{col:03d}_{idx}_{b:02d} 0 bpf_c{col:03d}_{idx} 0) vcvs gain={igain:.12e}\n")
                    f.write(f"SMIXI_c{col:03d}_{idx}_{b:02d} (mix_i_src_c{col:03d}_{idx}_{b:02d} mix_i_c{col:03d}_{idx} win_{idx}_{b:02d} 0) relay vt1=-1m vt2=1m ropen=ropen_mix rclosed=rclosed_mix\n")
                    f.write(f"EMIXQ_c{col:03d}_{idx}_{b:02d} (mix_q_src_c{col:03d}_{idx}_{b:02d} 0 bpf_c{col:03d}_{idx} 0) vcvs gain={qgain:.12e}\n")
                    f.write(f"SMIXQ_c{col:03d}_{idx}_{b:02d} (mix_q_src_c{col:03d}_{idx}_{b:02d} mix_q_c{col:03d}_{idx} win_{idx}_{b:02d} 0) relay vt1=-1m vt2=1m ropen=ropen_mix rclosed=rclosed_mix\n")
                f.write(f"RMIXI_c{col:03d}_{idx} (mix_i_c{col:03d}_{idx} 0) resistor r=1G\n")
                f.write(f"RMIXQ_c{col:03d}_{idx} (mix_q_c{col:03d}_{idx} 0) resistor r=1G\n")
                f.write(f"RINTI_c{col:03d}_{idx} (mix_i_c{col:03d}_{idx} Icar_c{col:03d}_{idx}) resistor r=1k\n")
                f.write(f"CINTI_c{col:03d}_{idx} (Icar_c{col:03d}_{idx} 0) capacitor c=80p\n")
                f.write(f"RINTQ_c{col:03d}_{idx} (mix_q_c{col:03d}_{idx} Qcar_c{col:03d}_{idx}) resistor r=1k\n")
                f.write(f"CINTQ_c{col:03d}_{idx} (Qcar_c{col:03d}_{idx} 0) capacitor c=80p\n")
                f.write(f"save bpf_c{col:03d}_{idx} Icar_c{col:03d}_{idx} Qcar_c{col:03d}_{idx}\n\n")
        f.write(f"tbtran tran stop=80n maxstep={maxstep}\n")
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=128)
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    out = write_tb(args.size, final=args.final or args.size == 128)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
