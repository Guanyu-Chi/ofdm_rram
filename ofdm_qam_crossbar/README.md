# OFDM QAM Crossbar Inference Evaluation

This directory contains the algorithm-level inference-accuracy evaluation code
for OFDM/QAM carrier-domain readout non-idealities.

## Main Entry Points

- [`main_binary.py`](main_binary.py): common training and evaluation entry.
- [`evaluation202502/MODEM.py`](evaluation202502/MODEM.py): computes the
  carrier-domain demodulation interference matrix.
- [`evaluation202502/run_inf_lenet_mnist_mismatch.sh`](evaluation202502/run_inf_lenet_mnist_mismatch.sh):
  LeNet-5 / MNIST inference sweep.
- [`evaluation202502/run_inf_vgg_cifar10_mismatch.sh`](evaluation202502/run_inf_vgg_cifar10_mismatch.sh):
  VGG / CIFAR-10 inference sweep.
- [`evaluation202502/run_inf_vgg_cifar100_mismatch.sh`](evaluation202502/run_inf_vgg_cifar100_mismatch.sh):
  VGG / CIFAR-100 inference sweep.

## Model Files

- [`models/lenet5.py`](models/lenet5.py): baseline LeNet-5 model.
- [`models/vgg_cifar10.py`](models/vgg_cifar10.py): baseline VGG-style model.
- [`models/lenet5_with_mismatch_carrier_v2.py`](models/lenet5_with_mismatch_carrier_v2.py):
  LeNet-5 model with carrier mismatch injected after convolution layers.
- [`models/vgg_cifar10_with_mismatch_carrier_v2.py`](models/vgg_cifar10_with_mismatch_carrier_v2.py):
  VGG-style model with carrier mismatch injected after convolution layers.
- [`models/binarized_modules.py`](models/binarized_modules.py): PyTorch binary
  layer utilities.

## Included Results

Lightweight inference logs are included under [`results_inference/`](results_inference/).
Datasets and pretrained checkpoint files are not included because of size.

## Experiment Layer Note

See [`EXPERIMENT_LAYER_NOTES.md`](EXPERIMENT_LAYER_NOTES.md) for the relationship
between this inference-accuracy evaluation and the separate circuit-level
128 x 128 RRAM crossbar verification flow.
