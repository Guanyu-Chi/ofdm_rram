import torch.nn as nn
import torchvision.transforms as transforms
import numpy as np
import torch
from MODEM import fdm_num, grid_step, f_async_bound, f_async_ratio_list, demodulation_matrix

f_async_ratio_list_tensor = torch.from_numpy(f_async_ratio_list).to('cuda')

def add_async_error_in_output(tensor, ratio_sigma):
    tensor_out = torch.zeros_like(tensor).to('cuda')
    
    shape = tensor.size()
    batch_size = shape[0]
    out_channel = shape[1]
    async_ratio_sampled = np.random.normal(loc=0, scale=1, size=(fdm_num*2, out_channel))
    async_ratio_sampled = torch.from_numpy(async_ratio_sampled).to('cuda')
    async_ratio_sampled = async_ratio_sampled * ratio_sigma
    # print(async_ratio_sampled)
    for ci in range(out_channel):
        for bi in range(batch_size//(fdm_num*2)):
            # calculate the demodulation correlation matrix
            for fi in range(fdm_num*2):
                async_ratio = async_ratio_sampled[fi, ci]
                async_ratio_index = torch.where(f_async_ratio_list_tensor > async_ratio)[0][0]
                async_ratio = f_async_ratio_list[async_ratio_index]
                for ffi in range(fdm_num*2):
                    tensor_out[bi*fdm_num*2+fi, ci] = tensor_out[bi*fdm_num*2+fi, ci] + tensor[bi*fdm_num*2+ffi, ci]*demodulation_matrix[async_ratio_index, fi, ffi]
    return tensor_out

tensor_test = torch.ones(4, 4)
print(tensor_test)
ratio_sigma_test = 0.00
tensor_out = add_async_error_in_output(tensor_test, ratio_sigma_test)
print(tensor_out)