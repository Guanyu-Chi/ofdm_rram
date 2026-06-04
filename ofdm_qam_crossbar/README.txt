#########################
# OFDM_QAM_crossbar
This Project   
|-- data/                                  # datasets
|-- evaluation202502/                      # evaluation scripts for this paper
|  |-- MODEM.py                            # script to simulate the modulation-demodulation errors, generates the interference factor matrix "demodulation_matrix" for NN inference use
|  |-- run_train.sh                        # bash script to launch training with arguments feeded
|  |-- run_inf_lenet_mnist_mismatch.sh     # bash script to launch inference with arguments feeded (with phase mismatch) (vgg8+cifar10)
|  |-- run_inf_vgg_cifar10_mismatch.sh     # bash script to launch inference with arguments feeded (with phase mismatch) (lenet+mnist)
|  |-- run_inf_vgg_cifar100_mismatch.sh    # bash script to launch inference with arguments feeded (with phase mismatch) (vgg8+cifar100)
|-- models/                                # model definitions
|  |-- lenet5.py                           # LeNet5 model (used for training)
|  |-- lenet5_with_mismatch_carrier_v2.py  # LeNet5 model with mismatched carrier (used for inference)
|  |-- vgg_cifar10.py                      # VGG8 model (used for training) (actually not binded with cifar10)
|  |-- vgg_cifar10_with_mismatch_carrier_v2.py   # VGG8 model with mismatched carrier (used for inference)
|-- results/                               # training results with saved trained models
|-- results_inference/                     # inference results (w/ non-ideality introduced)
|  |-- lenet5_mnist_mismatch/              # inference results for LeNet5+MNIST with mismatched carrier
|  |  |-- sigma0pxxx/                      # with the standard deviation of the phase noise set to 0.xxx
|  |-- vgg_cifar10_mismatch/               # inference results for VGG8+CIFAR10 with mismatched carrier
|  |-- vgg_cifar100_mismatch/              # inference results for VGG8+CIFAR100 with mismatched carrier  
|-- data.py                                # module, load dataset
|-- main_binary.py                         # the main python script
|-- preprocess.py                          # module, preprocess data
|-- utils.py                               # module, some utility functions
|-- README.md

# environment settings
python 3.8.10
pytorch 2.4.1

# how to run, take lenet+mnist as an example
1. open "run_inf_lenet_mnist_mismatch.sh"
2. modify the path at the first line.
3. properly set the arguments in the script
4. Go.
    - it will start to run multiple inference with different sigma values, the pretrained model without hardware non-ideality will be loaded. Each inference will take approx. 5 min.
5. check the results in "results_inference/lenet5_mnist_mismatch/

