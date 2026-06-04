# Experiment Layer Notes

This directory contains the algorithm-level inference-accuracy evaluation code
used to study carrier-domain non-idealities in neural-network inference.

The repository also contains a separate circuit-level 128 x 128 RRAM crossbar
verification flow under `experiments/iccd2026_ofdm_rram/`. The two parts are
connected by the OFDM-based readout concept, but they evaluate different layers
of the design.

你现在论文里两种都写到了，但对应的是两个不同实验层级：

1. accuracy / inference evaluation 写的是普通模型
2. circuit-level 128×128 RRAM crossbar 写的是 binary conductance / binary weight

也就是说，论文目前不是一个完全统一的 “binary neural network mapped to RRAM” 故事.

## Accuracy / Inference Evaluation

The inference-accuracy part uses ordinary PyTorch CNN layers and injects the
carrier-domain demodulation interference at convolution outputs.

Relevant files:

- [`main_binary.py`](main_binary.py): training/evaluation entry point.
- [`evaluation202502/MODEM.py`](evaluation202502/MODEM.py): builds the
  carrier-domain demodulation interference matrix.
- [`models/lenet5_with_mismatch_carrier_v2.py`](models/lenet5_with_mismatch_carrier_v2.py):
  LeNet-5 inference model with carrier mismatch injected after convolution
  layers.
- [`models/vgg_cifar10_with_mismatch_carrier_v2.py`](models/vgg_cifar10_with_mismatch_carrier_v2.py):
  VGG-style inference model with carrier mismatch injected after convolution
  layers.
- [`results_inference/`](results_inference/): lightweight inference logs and
  result files.

In this layer, the convolution output is treated as the ideal crossbar MVM
readout result. The OFDM/QAM demodulation mismatch model then perturbs that
output before the remaining neural-network layers continue inference.

## Binary Model Code

The directory also includes binary-network modules:

- [`models/binarized_modules.py`](models/binarized_modules.py)
- [`models/lenet5_binary.py`](models/lenet5_binary.py)
- [`models/vgg_cifar10_binary.py`](models/vgg_cifar10_binary.py)

These files implement binary weights and activations at the PyTorch model
level. They do not generate SPICE RRAM conductance matrices.

## Circuit-Level 128 x 128 Crossbar Verification

The circuit-level flow is stored outside this directory:

- [`../experiments/iccd2026_ofdm_rram/`](../experiments/iccd2026_ofdm_rram/)
- [`../review_package/`](../review_package/)

That flow verifies a generated 128 x 128 programmed read-state RRAM crossbar.
The generated conductance matrix uses binary Ron/Roff resistors and an NMOS
selector in each cell. The readout verification includes per-bitline readout,
BPF paths, coherent I/Q demodulation, integration, waveform exports, and
read-state performance extraction.

## Relationship Between the Two Parts

The inference-accuracy code answers how carrier-domain demodulation errors
affect CNN accuracy at the algorithm level. The 128 x 128 circuit flow answers
whether the generated OFDM-based RRAM readout path is structurally consistent,
executable in Spectre, and measurable at the circuit/read-state level.

Together, the two flows provide complementary evidence: algorithm-level
inference robustness and circuit-level readout verification.
