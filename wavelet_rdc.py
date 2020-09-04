#%%
import pywt as wt
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wv
import math



# functions
#%%
def threshold_generate(coeff_package):
    std = np.average(np.abs(coeff_package))/0.6745
    N = coeff_package.size
    T = std * math.sqrt(2 * math.log10(N))
    return T


# reading in...
# %%
(sr, data) = wv.read('lecture_spec.wav')
plot_index = np.arange(0, data.size)
plt.subplot(2, 1, 1)
plt.plot(plot_index[0:1000], data[0:1000]);plt.xlabel('time');plt.ylabel('mag');plt.title('original')
plt.show()


# Discrete wavelet transform
# %%
wavelet = wt.Wavelet('db10')
maxlev = wt.dwt_max_level(len(data), wavelet.dec_len)   # max level of decomposition changes based on the chosen wavelet
coeffs = wt.wavedec(data, wavelet, level=4)


# thresholding...
# %%
for i in range(1, len(coeffs)):
    threshold = threshold_generate(coeffs[i])
    print(threshold)
    coeffs[i] = wt.threshold(coeffs[i], threshold, mode='soft')     # 原本threshold他定的只是比例而已，這邊真正把他換成一個實際數字

# reconstructing
# %%
datarec = wt.waverec(coeffs, 'db10')
datarec = datarec.astype('int16')

# plot and ouput
#%%
plt.plot(plot_index[0:1000], datarec[0:1000]);plt.xlabel('time');plt.ylabel('mag');plt.title('denoised')
plt.show()
wv.write('lecture_wavlet.wav', sr, datarec)



