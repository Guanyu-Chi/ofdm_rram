cd /nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/
# python3 main_binary.py --dataset 'cifar10' --model 'vgg_cifar10' --save "vgg_cifar10" --epochs 50
python3 main_binary.py --dataset 'mnist' --model 'lenet5' --save "lenet5_mnist" --epochs 50
# python3 main_binary.py --dataset 'cifar100' --model 'vgg_cifar10' --save "vgg_cifar100" --epochs 50 --num_class 100 --gpus '1'