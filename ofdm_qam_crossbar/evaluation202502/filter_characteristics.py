import numpy as np
from scipy.interpolate import interp1d
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import pandas as pd

fdm_num = 4
fdm_freq_range = [1e8, 1e9]
freq_total_range = [1e7, 1e10]

freq_point_list = np.logspace(np.log10(fdm_freq_range[0]), np.log10(fdm_freq_range[1]), num=fdm_num)
print(freq_point_list)

# filter 
filter_parameters = []

mc_num = 1000
freq_drift_ratio_std = 0.1

for fi in range(fdm_num):
    freq = freq_point_list[fi]
    filter_parameters.append({'freq': freq, 'C': None, 'R': None})
    Resistance = 1e4
    Capacitance = 1/(2*np.pi*freq*Resistance)
    filter_parameters[fi]['C'] = Capacitance
    filter_parameters[fi]['R'] = Resistance
    # # high-pass filter
    # freq_sweep = np.logspace(np.log10(freq_total_range[0]), np.log10(freq_total_range[1]), num=3000)
    # H = Resistance / (Resistance + 1/(1j*2*np.pi*freq_sweep*Capacitance)) * np.sqrt(2) # normalized to 1
    # H_mag = np.abs(H)
    # freq_interested = [freq*0.9, freq, freq*1.1]
    # H_mag_interested = np.interp(freq_interested, freq_sweep, H_mag)
    # print(H_mag_interested)
    # # find the 3dB point
    freq_drifted_list = []
    H_mag_with_freq_drifted_list = []
    for mi in range(mc_num):
        freq_drifted = np.random.lognormal(mean=np.log(freq), sigma=freq_drift_ratio_std*np.log(freq))

        

    