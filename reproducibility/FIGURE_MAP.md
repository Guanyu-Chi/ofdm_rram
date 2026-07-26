# Figure and Table Provenance

Every figure and table in the manuscript, with its generating script, its data
source, the command that produces it, and why it is drawn that way.

## Figures

| Fig | File | Script | Data source | Rationale |
|-----|------|--------|-------------|-----------|
| 1 | `overview.png` | conceptual (hand-drawn) | — | OFDM I/Q-encoding principle; schematic only, no measured data |
| 2 | `mapping.png` | conceptual (hand-drawn) | — | Gray-coded I/Q amplitude mapping; schematic only |
| 3 | `cim_repro.pdf` | `make_cim_png_repro.py` | block diagram | full architecture with the three modeling levels annotated (transistor / compact-RRAM / behavioral), so scope is unambiguous |
| 4a | `fig_leakage_heatmap_v5.png` | `make_paper_figures.py` | `filteronly_leakage_matrix_v5.csv` | per-row-normalized heatmap makes the diagonal (correct channel) and off-diagonal leakage read at a glance |
| 4b | `fig_decision_margins_v5.png` | `make_paper_figures.py` | `ideal_decision_margin_v5.csv`, `gilbert_channel_margin_v5.csv` | grouped bars compare ideal vs transistor-level margin per channel against the 3x floor |
| 5 | `fig_cim_endtoend_waveform.pdf` | `make_cim_waveform_fig.py` | `rramcim_4x4_v5_ascii` | stacked transient (WL / bitline / filter / baseband) shows the signal surviving each stage; shaded 20 ns integration window marks where the decision is read |
| 6 | `fig_hwacc_networks.pdf` | `make_hwacc_figure.py` | `hw_aware_network_accuracy.csv` | grouped bars over 4 networks compare baseline / measured-crosstalk / harmonic-calibrated, showing the depth-compounding effect |
| 7 | `fig_rram_variation.pdf` | `make_rram_variation_fig.py` | `rram_variation_accuracy.csv` | accuracy-vs-sigma line plot shows all networks degrade gently, so device variation is secondary to the carrier harmonic |

## Tables

| Table | Content | Where the data comes from |
|-------|---------|---------------------------|
| 1 | Measurement setup and key parameters | Read directly from the netlists in `netlists/`; all values are collected in `PARAMETERS.md`. No script is needed. |
| 2 | Measured four-channel chain summary (carrier error, filter gain, mixer gain, margins) | `oscillator_calibration.csv`, `filteronly_leakage_matrix_v5.csv`, `gilbert_c1_metrics_v5.csv`, `gilbert_channel_margin_v5.csv` (produced by `analyze_gilbert.py` and `build_filteronly_matrix.py`) |
| 3 | Per-network accuracy under the measured hardware model | `hw_aware_network_accuracy.csv` |
| 4 | Performance comparison (throughput gain, energy efficiency) | Throughput and energy are computed by hand from the measured steady-state power in `power_4tone_v5.csv` and the operation count; the resulting values are collected in `performance_measured_v6.csv`. No dedicated figure script. |

## In-text numbers

- Carrier 249.50 / 498.92 / 748.86 / 998.70 MHz (<=0.22% error): `oscillator_calibration.csv`
- Filter diagonal 40.7 / 145.4 / 93.7 / 66.5 mV: `filteronly_leakage_matrix_v5.csv`
- Ideal margins 24.0 / 17.4 / 3.67 / 20.8; Gilbert 9.9 / 15.2 / 2.96 / 9.3: margin CSVs
- 4x4 MVM: ON 14.0 uA, OFF <=2.07 uA (14.8%): `rram_measured_mvm.csv`, `rram_mvm_error.csv`
- Network accuracy 97.9/99.6/90.6/67.3 -> 73.2/26.4/49.8/27.9 -> 91.8/39.0/69.4/42.2: `hw_aware_network_accuracy.csv`
- Power 14.43 mW steady / 13.58 mW idle: `power_4tone_v5.csv`
- Throughput 0.80 GbOP/s/BL measured, 102.4 projected (41.6x/7.2x/1.1x): `performance_measured_v6.csv`
