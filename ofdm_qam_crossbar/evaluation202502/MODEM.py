import numpy as np
from scipy.interpolate import interp1d
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import pandas as pd

# this file computes the interference factor of synchronized demodulation with some mismatches in the carriers used by the demodulator.
# -> carriers generator (e.g., 50M 100M)
# -> modulate with the generated carriers (possible noise & phase drift)
# -> signal transmit throught the crossbar (distort caused by the array non-linearity, result in phase drift in different signal component)
# -> demodulation: synchronized demodulation using the received distorted signal and the carriers (also with some distortions due to the trasmit from the carrier generator), resulting in non-ideal demodulation (channel interference)

fdm_num = 2
#running two carries once 
f0 = 50e6 #50M
freq_list = [f0*i for i in range(1, fdm_num+1)] #50M and 100M
fsample_for_simu = 100*max(freq_list) #sample rate for this simulation, discretize the waves
period_list = [1/i for i in freq_list] 
symbol_interval = max(period_list)*2 # the time interval of a message frame in RF communication, must be integer multiple of the carrier period, set as 2x here
# f_mismatch_ratio_std = 0.01
# f_mismatch_ratio = np.random.normal(1, f_mismatch_ratio_std, fdm_num)
# freq_list_async = [f0*i for i in f_mismatch_ratio]

num_sampled_points = symbol_interval*fsample_for_simu
t = np.linspace(0, symbol_interval, int(num_sampled_points))

signal_list = []
for fi in range(fdm_num):
    signal_cos = np.cos(2*np.pi*freq_list[fi]*t)
    signal_sin = np.sin(2*np.pi*freq_list[fi]*t)
    signal_list.append(signal_cos)
    signal_list.append(signal_sin)
    # plt.plot(t, signal_sin)
    # break

grid_step = 0.0001
f_mismatch_bound = [-0.5, 0.5] # degree of mismatch
f_mismatch_ratio_list = np.linspace(-0.5, 0.5, 10001)
# f_mismatch_ratio_list = [0]
sync_demodulation = []

# print(f_mismatch_ratio_list)
# print(np.where(f_mismatch_ratio_list==0.401))

demodulation_matrix = np.zeros((len(f_mismatch_ratio_list) ,len(signal_list), len(signal_list)))
# for f_mismatch_ratio in f_mismatch_ratio_list:
for fa in range(len(f_mismatch_ratio_list)):
    # fa is the f_mismatch_ratio in the f_mismatch_ratio_list
    f_mismatch_ratio = f_mismatch_ratio_list[fa]
    mismatch_signal_list = []
    # if f_mismatch_ratio = 0
    if f_mismatch_ratio < grid_step and f_mismatch_ratio > -grid_step:
        
        for i in range(len(signal_list)):
            for j in range(len(signal_list)):
                if i==j:
                    demodulation_matrix[fa][i][j] = 1
                else:
                    demodulation_matrix[fa][i][j] = 0
        continue
    # generate mismatch signal
    for fi in range(fdm_num):
        signal_cos = np.cos(2*np.pi*freq_list[fi]*t+2*np.pi*f_mismatch_ratio)
        signal_sin = np.sin(2*np.pi*freq_list[fi]*t+2*np.pi*f_mismatch_ratio)
        mismatch_signal_list.append(signal_cos)
        mismatch_signal_list.append(signal_sin)
        # plt.plot(t, signal_sin)
        # break

    # demodulation, 4x4 matrix
    # demodulation_matrix = np.zeros((len(signal_list), len(mismatch_signal_list)))
    for i in range(len(signal_list)):
        for j in range(len(mismatch_signal_list)):
            demodulation_matrix[fa][i][j] = np.dot(signal_list[i], mismatch_signal_list[j]) \
            *(symbol_interval/num_sampled_points) / (symbol_interval/2) # *normalization factor
            # print('demodule')
    # print("ratio: ", f_mismatch_ratio)
    # print(demodulation_matrix[fa])

# plt.savefig('signal.png')
