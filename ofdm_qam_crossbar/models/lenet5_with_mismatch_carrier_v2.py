import torch.nn as nn
import torchvision.transforms as transforms
import numpy as np
import torch
import sys
sys.path.append('/nas/ei/share/TUEIEDAscratch/ge86duw/BNN_OFDM_QAM/evaluation202502/')
# from MODEM import fdm_num, grid_step, f_mismatch_bound, f_mismatch_ratio_list, demodulation_matrix
from MODEM import fdm_num, f_mismatch_ratio_list, demodulation_matrix

f_mismatch_ratio_list_tensor = torch.from_numpy(f_mismatch_ratio_list).to('cuda')

class AlexNetOWT_BN(nn.Module):

    def __init__(self, num_classes=1000, sigma=0):
        super(AlexNetOWT_BN, self).__init__()

        # lenet5 layers
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5, stride=1)
        self.bn1 = nn.BatchNorm2d(6)
        self.relu1 = nn.ReLU(inplace=True)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5, stride=1)
        self.bn2 = nn.BatchNorm2d(16)
        self.relu2 = nn.ReLU(inplace=True)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.bn3 = nn.BatchNorm1d(120)
        self.relu3 = nn.ReLU(inplace=True)
        self.fc2 = nn.Linear(120, 84)
        self.bn4 = nn.BatchNorm1d(84)
        self.relu4 = nn.ReLU(inplace=True)
        self.fc3 = nn.Linear(84, num_classes)
        self.logsoftmax = nn.LogSoftmax()

        self.sigma = sigma

        self.regime = {
            0: {'optimizer': 'SGD', 'lr': 1e-2,
                'weight_decay': 5e-4, 'momentum': 0.9},
            10: {'lr': 5e-3},
            15: {'lr': 1e-3, 'weight_decay': 0},
            20: {'lr': 5e-4},
            25: {'lr': 1e-4}
        }

    def add_mismatch_error_in_output(self, tensor, ratio_sigma):
        tensor_out = torch.zeros_like(tensor).to('cuda')
        
        shape = tensor.size()
        batch_size = shape[0]
        out_channel = shape[1]
        mismatch_ratio_sampled = np.random.normal(loc=0, scale=1, size=fdm_num*2)
        mismatch_ratio_sampled = torch.from_numpy(mismatch_ratio_sampled).to('cuda')
        mismatch_ratio_sampled = mismatch_ratio_sampled * ratio_sigma
        # print(mismatch_ratio_sampled)
        for bi in range(batch_size//(fdm_num*2)):
            # calculate the demodulation correlation matrix
            for fi in range(fdm_num*2):
                mismatch_ratio = mismatch_ratio_sampled[fi]
                mismatch_ratio_index = torch.where(f_mismatch_ratio_list_tensor > mismatch_ratio)[0][0]
                mismatch_ratio = f_mismatch_ratio_list[mismatch_ratio_index]
                for ffi in range(fdm_num*2):
                    tensor_out[bi*fdm_num*2+fi] = tensor_out[bi*fdm_num*2+fi] + tensor[bi*fdm_num*2+ffi]*demodulation_matrix[mismatch_ratio_index, fi, ffi]
        return tensor_out

    def forward(self, x):
        sigma_value = self.sigma

        x = self.conv1(x)
        x = self.add_mismatch_error_in_output(x, sigma_value)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.add_mismatch_error_in_output(x, sigma_value)
        x = self.bn2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        x = x.view(-1, 16 * 4 * 4)
        x = self.fc1(x)
        x = self.bn3(x)
        x = self.relu3(x)
        x = self.fc2(x)
        x = self.bn4(x)
        x = self.relu4(x)
        x = self.fc3(x)
        x = self.logsoftmax(x)

        return x


def lenet5_with_mismatch_carrier_v2(**kwargs):
    num_classes = kwargs.get( 'num_classes', 1000)
    sigma = kwargs.get('sigma', 0)
    return AlexNetOWT_BN(num_classes, sigma)
