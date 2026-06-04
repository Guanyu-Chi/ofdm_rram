cd /nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/
# python3 main_binary.py --dataset 'cifar10' --model 'vgg_cifar10' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/results/vgg_cifar10/model_best.pth.tar"  --save "vgg_cifar10"
python3 main_binary.py --dataset 'cifar10' --model 'vgg_cifar10_with_async_carrier' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/results/vgg_cifar10/model_best.pth.tar"  --save "vgg_cifar10" --sigma 0.0


# python3 main_binary.py --dataset 'mnist' --model 'lenet5_with_freq_drift' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BinaryNet.pytorch/results/lenet5_mnist/model_best.pth.tar" --save "./lenet5_mnist/sigma=0.1" --sigma 0.1 --num_class 10
# python3 main_binary.py --dataset 'mnist' --model 'lenet5_with_freq_drift' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BinaryNet.pytorch/results/lenet5_mnist/model_best.pth.tar" --save "./lenet5_mnist/sigma=0.3" --sigma 0.3 --num_class 10
# python3 main_binary.py --dataset 'mnist' --model 'lenet5_with_freq_drift' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BinaryNet.pytorch/results/lenet5_mnist/model_best.pth.tar" --save "./lenet5_mnist/sigma=0.5" --sigma 0.5 --num_class 10

# python3 main_binary.py --dataset 'mnist' --model 'lenet5_binary' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/results/lenet5_binary_mnist/model_best.pth.tar" --save "./lenet5_binary_mnist/sigma=0" 
# python3 main_binary.py --dataset 'mnist' --model 'lenet5_binary' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/results/lenet5_binary_mnist_2/model_best.pth.tar" --save "./lenet5_binary_mnist_2/sigma=0" 