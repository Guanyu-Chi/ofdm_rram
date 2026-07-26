# FiQ-CIM Reproducibility Package

This package reproduces every measured circuit result and network-evaluation
result reported in the FiQ-CIM manuscript (frequency-multiplexed RRAM-CIM with
orthogonal I/Q component encoding). It contains the frozen SPICE netlists, the
parsing and figure-generation scripts, the result tables behind every figure,
and the trained model used for the network study. Every figure and every
number in the paper is traceable to a named netlist and a named CSV
(see `FIGURE_MAP.md`).

Raw Spectre transient dumps (nutascii, hundreds of MB each) are **not** shipped;
they are regenerated from the netlists with the commands below.

## Directory structure

```
reproducibility/
├── README.md            this file
├── FIGURE_MAP.md        every figure/table -> script + data + command + rationale
├── PARAMETERS.md        all frozen circuit parameters in one place
├── env/
│   ├── requirements.txt Python dependencies
│   └── tools.txt        Spectre / device-model versions
├── netlists/            10 Cadence Spectre .scs testbenches (frozen parameters)
├── scripts/             14 parsing / analysis / figure-generation scripts
├── data/                24 result CSVs (calibration, matrices, margins, MVM, accuracy, power)
├── figures/             final paper figures (PDF + PNG)
└── models/              resnet20_mnist_model_best.pth.tar (trained in this work)
```

## Environment

- **Circuit**: Cadence Spectre 15.1.0.627, CPU transient, PTM 45 nm BSIM4
  compact models (`models/ptm45/`, not redistributed here — public predictive
  models). See `env/tools.txt`.
- **Analysis / figures**: Python 3, see `env/requirements.txt`
  (numpy, matplotlib, torch, torchvision, pillow).

## End-to-end reproduction

The pipeline is: (1) run a Spectre transient to produce a nutascii waveform,
(2) parse it to a CSV, (3) render the figure. Each stage is one command.

### 1. Filter-bank leakage matrix and decision margins (paper Fig. 4)

```
cd netlists
# four single-tone runs (differ only in the enabled DAC bits) + four-tone run
for tag in 250 425 723 1229 4tone; do
  spectre tb_ptm45_filteronly_${tag}.scs +escchars -format nutascii -raw ../${tag}_ascii
done
cd ../scripts
for tag in 250 425 723 1229; do
  python parse_filteronly_matrix.py ../${tag}_ascii --stim $tag --out ../data/filteronly_matrix_stim${tag}_v5.csv
done
python build_filteronly_matrix.py _v5           # -> filteronly_leakage_matrix_v5.csv
python ideal_demod.py --runs 250=../250_ascii 425=../425_ascii 723=../723_ascii 1229=../1229_ascii --t0 160e-9 --suffix _v5
python analyze_gilbert.py v5                     # -> gilbert_*_v5.csv
python make_paper_figures.py                     # -> fig_leakage_heatmap_v5, fig_decision_margins_v5
```

### 2. End-to-end RRAM-CIM transient (paper Fig. 5)

```
cd netlists
spectre tb_ptm45_rramcim_4x4.scs     +escchars -format nutascii -raw ../rramcim_4x4_v5_ascii
spectre tb_ptm45_rramcim_4x4_pwr.scs +escchars -format nutascii -raw ../rramcim_4x4_pwr_ascii   # adds VDD:p probe
cd ../scripts
python make_cim_waveform_fig.py                  # -> fig_cim_endtoend_waveform
# rram_*.csv (programmed / expected / measured MVM) are produced by the analysis in EXPERIMENT_SUMMARY
```

### 3. Hardware-aware network accuracy (paper Fig. 6, Table 3)

```
cd scripts
python train_resnet20_mnist.py                   # -> models/resnet20_mnist_model_best.pth.tar (LeNet5/VGG8 reuse released checkpoints)
python hw_aware_network_eval.py                  # -> hw_aware_network_accuracy.csv
python make_hwacc_figure.py                      # -> fig_hwacc_networks
```

### 4. RRAM conductance-variation study (paper Fig. 7)

```
cd scripts
python rram_variation_eval.py                    # -> rram_variation_accuracy.csv
python make_rram_variation_fig.py                # -> fig_rram_variation
```

### 5. Architecture figure (paper Fig. 3)

```
cd scripts
python make_cim_png_repro.py                     # -> cim_repro.pdf / cim_repro.png (hand-drawn block diagram)
```

## Traceability

Each reported quantity maps to a CSV in `data/`:

- carrier frequencies / errors -> `oscillator_calibration.csv`
- filter-only 4x4 leakage -> `filteronly_leakage_matrix_v5.csv`
- ideal vs Gilbert decision margins -> `ideal_decision_margin_v5.csv`, `gilbert_channel_margin_v5.csv`
- 4x4 crossbar MVM -> `rram_{programmed_matrix,input_vector,expected_mvm,measured_mvm,mvm_error}.csv`
- network accuracy -> `hw_aware_network_accuracy.csv`, `rram_variation_accuracy.csv`
- performance / power -> `performance_measured_v6.csv`, `power_4tone_v5.csv`

Frozen circuit parameters are listed in `PARAMETERS.md`.
