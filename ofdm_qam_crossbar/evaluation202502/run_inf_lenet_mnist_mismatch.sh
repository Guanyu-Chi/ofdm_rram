cd /nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/
# python3 main_binary.py --dataset 'cifar10' --model 'vgg_cifar10' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/results/vgg_cifar10/model_best.pth.tar"  --save "vgg_cifar10"
python3 main_binary.py --dataset 'mnist' --model 'lenet5_with_mismatch_carrier_v2' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/results/lenet5_mnist/model_best.pth.tar"  --save "lenet5_mnist_mismatch/sigma0p000" --sigma 0.000
python3 main_binary.py --dataset 'mnist' --model 'lenet5_with_mismatch_carrier_v2' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/results/lenet5_mnist/model_best.pth.tar"  --save "lenet5_mnist_mismatch/sigma0p005" --sigma 0.005
python3 main_binary.py --dataset 'mnist' --model 'lenet5_with_mismatch_carrier_v2' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/results/lenet5_mnist/model_best.pth.tar"  --save "lenet5_mnist_mismatch/sigma0p010" --sigma 0.010
python3 main_binary.py --dataset 'mnist' --model 'lenet5_with_mismatch_carrier_v2' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/results/lenet5_mnist/model_best.pth.tar"  --save "lenet5_mnist_mismatch/sigma0p015" --sigma 0.015
python3 main_binary.py --dataset 'mnist' --model 'lenet5_with_mismatch_carrier_v2' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/results/lenet5_mnist/model_best.pth.tar"  --save "lenet5_mnist_mismatch/sigma0p020" --sigma 0.020
python3 main_binary.py --dataset 'mnist' --model 'lenet5_with_mismatch_carrier_v2' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/results/lenet5_mnist/model_best.pth.tar"  --save "lenet5_mnist_mismatch/sigma0p025" --sigma 0.025
python3 main_binary.py --dataset 'mnist' --model 'lenet5_with_mismatch_carrier_v2' --evaluate "/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/results/lenet5_mnist/model_best.pth.tar"  --save "lenet5_mnist_mismatch/sigma0p030" --sigma 0.030

