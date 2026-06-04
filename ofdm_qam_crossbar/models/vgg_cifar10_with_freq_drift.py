import torch.nn as nn
import torchvision.transforms as transforms
import numpy as np
import torch

class AlexNetOWT_BN(nn.Module):

    def __init__(self, num_classes=1000, sigma=0):
        super(AlexNetOWT_BN, self).__init__()
        # self.features = nn.Sequential(
        #     nn.Conv2d(3, 128, kernel_size=3, stride=1, padding=1,
        #               bias=False),
        #     nn.BatchNorm2d(128),
        #     nn.ReLU(inplace=True),

        #     nn.Conv2d(128, 128, kernel_size=3, padding=1, bias=False),
        #     nn.MaxPool2d(kernel_size=2, stride=2),
        #     nn.ReLU(inplace=True),
        #     nn.BatchNorm2d(128),

        #     nn.Conv2d(128, 256, kernel_size=3, padding=1, bias=False),
        #     nn.ReLU(inplace=True),
        #     nn.BatchNorm2d(256),

        #     nn.Conv2d(256, 256, kernel_size=3, padding=1, bias=False),
        #     nn.MaxPool2d(kernel_size=2, stride=2),
        #     nn.ReLU(inplace=True),
        #     nn.BatchNorm2d(256),

        #     nn.Conv2d(256, 512, kernel_size=3, padding=1, bias=False),
        #     nn.ReLU(inplace=True),
        #     nn.BatchNorm2d(512),

        #     nn.Conv2d(512, 512, kernel_size=3, padding=1, bias=False),
        #     nn.MaxPool2d(kernel_size=2, stride=2),
        #     nn.ReLU(inplace=True),
        #     nn.BatchNorm2d(512),
        # )
        self.sigma = sigma

        self.conv1 = nn.Conv2d(3, 128, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(128)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(128, 128, kernel_size=3, padding=1, bias=False)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.relu2 = nn.ReLU(inplace=True)
        self.bn2 = nn.BatchNorm2d(128)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1, bias=False)
        self.relu3 = nn.ReLU(inplace=True)
        self.bn3 = nn.BatchNorm2d(256)
        self.conv4 = nn.Conv2d(256, 256, kernel_size=3, padding=1, bias=False)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.relu4 = nn.ReLU(inplace=True)
        self.bn4 = nn.BatchNorm2d(256)
        self.conv5 = nn.Conv2d(256, 512, kernel_size=3, padding=1, bias=False)
        self.relu5 = nn.ReLU(inplace=True)
        self.bn5 = nn.BatchNorm2d(512)
        self.conv6 = nn.Conv2d(512, 512, kernel_size=3, padding=1, bias=False)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.relu6 = nn.ReLU(inplace=True)
        self.bn6 = nn.BatchNorm2d(512)

        # self.classifier = nn.Sequential(
        #     nn.Linear(512 * 4 * 4, 1024, bias=False),
        #     nn.BatchNorm1d(1024),
        #     nn.ReLU(inplace=True),
        #     nn.Dropout(0.5),
        #     nn.Linear(1024, 1024, bias=False),
        #     nn.BatchNorm1d(1024),
        #     nn.ReLU(inplace=True),
        #     nn.Dropout(0.5),
        #     nn.Linear(1024, num_classes),
        #     nn.LogSoftMax()
        # )
        self.fc1 = nn.Linear(512 * 4 * 4, 1024, bias=False) 
        self.bn7 = nn.BatchNorm1d(1024)
        self.relu7 = nn.ReLU(inplace=True)
        self.dropout1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(1024, 1024, bias=False)
        self.bn8 = nn.BatchNorm1d(1024)
        self.relu8 = nn.ReLU(inplace=True)
        self.dropout2 = nn.Dropout(0.5)
        self.fc3 = nn.Linear(1024, num_classes)
        self.logsoftmax = nn.LogSoftmax()

        self.regime = {
            0: {'optimizer': 'SGD', 'lr': 1e-2,
                'weight_decay': 5e-4, 'momentum': 0.9},
            10: {'lr': 5e-3},
            15: {'lr': 1e-3, 'weight_decay': 0},
            20: {'lr': 5e-4},
            25: {'lr': 1e-4}
        }

    def forward(self, x):
        # x = self.features(x)
        # x = x.view(-1, 512 * 4 * 4)
        # x = self.classifier(x)
        # return x
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
        x = self.conv2(x)
        factor = np.random.lognormal(mean=0, sigma=sigma_value, size=x.size())
        factor = torch.from_numpy(factor).float().to('cuda').detach()
        factor_complex = torch.complex(factor, torch.zeros_like(factor)).to('cuda')
        # tensor_j = torch.complex(torch.zeros_like(factor), torch.ones_like(factor)).to('cuda')
        H_filter = (1/(1 - 1j*factor_complex)).to('cuda')
        H_mag = torch.abs(H_filter) * torch.sqrt(torch.tensor(2.0)).to('cuda')
        H_mag = H_mag.to('cuda')
        x = x * H_mag
        x = self.pool1(x)
        x = self.relu2(x)
        x = self.bn2(x)
        x = self.conv3(x)
        factor = np.random.lognormal(mean=0, sigma=sigma_value, size=x.size())
        factor = torch.from_numpy(factor).float().to('cuda').detach()
        factor_complex = torch.complex(factor, torch.zeros_like(factor)).to('cuda')
        # tensor_j = torch.complex(torch.zeros_like(factor), torch.ones_like(factor)).to('cuda')
        H_filter = (1/(1 - 1j*factor_complex)).to('cuda')
        H_mag = torch.abs(H_filter) * torch.sqrt(torch.tensor(2.0)).to('cuda')
        H_mag = H_mag.to('cuda')
        x = x * H_mag
        x = self.relu3(x)
        x = self.bn3(x)
        x = self.conv4(x)
        factor = np.random.lognormal(mean=0, sigma=sigma_value, size=x.size())
        factor = torch.from_numpy(factor).float().to('cuda').detach()
        factor_complex = torch.complex(factor, torch.zeros_like(factor)).to('cuda')
        # tensor_j = torch.complex(torch.zeros_like(factor), torch.ones_like(factor)).to('cuda')
        H_filter = (1/(1 - 1j*factor_complex)).to('cuda')
        H_mag = torch.abs(H_filter) * torch.sqrt(torch.tensor(2.0)).to('cuda')
        H_mag = H_mag.to('cuda')
        x = x * H_mag
        x = self.pool2(x)
        x = self.relu4(x)
        x = self.bn4(x)
        x = self.conv5(x)
        factor = np.random.lognormal(mean=0, sigma=sigma_value, size=x.size())
        factor = torch.from_numpy(factor).float().to('cuda').detach()
        factor_complex = torch.complex(factor, torch.zeros_like(factor)).to('cuda')
        # tensor_j = torch.complex(torch.zeros_like(factor), torch.ones_like(factor)).to('cuda')
        H_filter = (1/(1 - 1j*factor_complex)).to('cuda')
        H_mag = torch.abs(H_filter) * torch.sqrt(torch.tensor(2.0)).to('cuda')
        H_mag = H_mag.to('cuda')
        x = x * H_mag
        x = self.relu5(x)
        x = self.bn5(x)
        x = self.conv6(x)
        factor = np.random.lognormal(mean=0, sigma=sigma_value, size=x.size())
        factor = torch.from_numpy(factor).float().to('cuda').detach()
        factor_complex = torch.complex(factor, torch.zeros_like(factor)).to('cuda')
        # tensor_j = torch.complex(torch.zeros_like(factor), torch.ones_like(factor)).to('cuda')
        H_filter = (1/(1 - 1j*factor_complex)).to('cuda')
        H_mag = torch.abs(H_filter) * torch.sqrt(torch.tensor(2.0)).to('cuda')
        H_mag = H_mag.to('cuda')
        x = x * H_mag
        x = self.pool3(x)
        x = self.relu6(x)
        x = self.bn6(x)
        x = x.view(-1, 512 * 4 * 4)
        x = self.fc1(x)
        factor = np.random.lognormal(mean=0, sigma=sigma_value, size=x.size())
        factor = torch.from_numpy(factor).float().to('cuda').detach()
        factor_complex = torch.complex(factor, torch.zeros_like(factor)).to('cuda')
        # tensor_j = torch.complex(torch.zeros_like(factor), torch.ones_like(factor)).to('cuda')
        H_filter = (1/(1 - 1j*factor_complex)).to('cuda')
        H_mag = torch.abs(H_filter) * torch.sqrt(torch.tensor(2.0)).to('cuda')
        H_mag = H_mag.to('cuda')
        x = x * H_mag
        x = self.bn7(x)
        x = self.relu7(x)
        x = self.dropout1(x)
        x = self.fc2(x)
        factor = np.random.lognormal(mean=0, sigma=sigma_value, size=x.size())
        factor = torch.from_numpy(factor).float().to('cuda').detach()
        factor_complex = torch.complex(factor, torch.zeros_like(factor)).to('cuda')
        # tensor_j = torch.complex(torch.zeros_like(factor), torch.ones_like(factor)).to('cuda')
        H_filter = (1/(1 - 1j*factor_complex)).to('cuda')
        H_mag = torch.abs(H_filter) * torch.sqrt(torch.tensor(2.0)).to('cuda')
        H_mag = H_mag.to('cuda')
        x = x * H_mag
        x = self.bn8(x)
        x = self.relu8(x)
        x = self.dropout2(x)
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


def vgg_cifar10_with_freq_drift(**kwargs):
    num_classes = kwargs.get( 'num_classes', 1000)
    sigma = kwargs.get('sigma', 0)
    return AlexNetOWT_BN(num_classes, sigma)
