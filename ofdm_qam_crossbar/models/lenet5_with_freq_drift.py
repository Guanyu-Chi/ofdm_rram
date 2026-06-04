import torch.nn as nn
import torchvision.transforms as transforms
import numpy as np
import torch

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

    def forward(self, x):
        sigma_value = self.sigma

        x = self.conv1(x)
        factor = np.random.lognormal(mean=0, sigma=sigma_value, size=x.size())
        factor = torch.from_numpy(factor).float().to('cuda').detach()
        factor_complex = torch.complex(factor, torch.zeros_like(factor)).to('cuda')
        # tensor_j = torch.complex(torch.zeros_like(factor), torch.ones_like(factor)).to('cuda')
        H_filter = (1/(1 - 1j*factor_complex)).to('cuda')
        H_mag = torch.abs(H_filter) * torch.sqrt(torch.tensor(2.0)).to('cuda')
        H_mag = H_mag.to('cuda')
        x = x * H_mag
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        factor = np.random.lognormal(mean=0, sigma=sigma_value, size=x.size())
        factor = torch.from_numpy(factor).float().to('cuda').detach()
        factor_complex = torch.complex(factor, torch.zeros_like(factor)).to('cuda')
        # tensor_j = torch.complex(torch.zeros_like(factor), torch.ones_like(factor)).to('cuda')
        H_filter = (1/(1 - 1j*factor_complex)).to('cuda')
        H_mag = torch.abs(H_filter) * torch.sqrt(torch.tensor(2.0)).to('cuda')
        H_mag = H_mag.to('cuda')
        x = x * H_mag
        x = self.bn2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        x = x.view(-1, 16 * 4 * 4)
        x = self.fc1(x)
        factor = np.random.lognormal(mean=0, sigma=sigma_value, size=x.size())
        factor = torch.from_numpy(factor).float().to('cuda').detach()
        factor_complex = torch.complex(factor, torch.zeros_like(factor)).to('cuda')
        # tensor_j = torch.complex(torch.zeros_like(factor), torch.ones_like(factor)).to('cuda')
        H_filter = (1/(1 - 1j*factor_complex)).to('cuda')
        H_mag = torch.abs(H_filter) * torch.sqrt(torch.tensor(2.0)).to('cuda')
        H_mag = H_mag.to('cuda')
        x = x * H_mag
        x = self.bn3(x)
        x = self.relu3(x)
        x = self.fc2(x)
        factor = np.random.lognormal(mean=0, sigma=sigma_value, size=x.size())
        factor = torch.from_numpy(factor).float().to('cuda').detach()
        factor_complex = torch.complex(factor, torch.zeros_like(factor)).to('cuda')
        # tensor_j = torch.complex(torch.zeros_like(factor), torch.ones_like(factor)).to('cuda')
        H_filter = (1/(1 - 1j*factor_complex)).to('cuda')
        H_mag = torch.abs(H_filter) * torch.sqrt(torch.tensor(2.0)).to('cuda')
        H_mag = H_mag.to('cuda')
        x = x * H_mag
        x = self.bn4(x)
        x = self.relu4(x)
        x = self.fc3(x)
        factor = np.random.lognormal(mean=0, sigma=sigma_value, size=x.size())
        factor = torch.from_numpy(factor).float().to('cuda').detach()
        factor_complex = torch.complex(factor, torch.zeros_like(factor)).to('cuda')
        # tensor_j = torch.complex(torch.zeros_like(factor), torch.ones_like(factor)).to('cuda')
        H_filter = (1/(1 - 1j*factor_complex)).to('cuda')
        H_mag = torch.abs(H_filter) * torch.sqrt(torch.tensor(2.0)).to('cuda')
        H_mag = H_mag.to('cuda')
        x = x * H_mag
        x = self.logsoftmax(x)

        return x


def lenet5_with_freq_drift(**kwargs):
    num_classes = kwargs.get( 'num_classes', 1000)
    sigma = kwargs.get('sigma', 0)
    return AlexNetOWT_BN(num_classes, sigma)
