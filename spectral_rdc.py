#%%
import numpy as np
from scipy.io import wavfile as wv
import   matplotlib.pyplot as plt
import audiolib as ad

#%%

# x_w(m) preprocessing
(framedata, frames) = ad.loadfile_and_frame('lecture.wav', 1024, 0.5)
ham = np.hanning(1024)
frame_mag = []
frame_angle = []

for i in range(len(frames)):
    frames[i] = frames[i] * ham
    frames[i] = np.fft.fft(frames[i])
    frame_mag.append(np.abs(frames[i]))
    frame_angle.append(np.angle(frames[i]))
    

# n_w(m) preprocessing
(framedata_n, noise_frames) = ad.loadfile_and_frame('noise.wav', 1024, 0.5)
fft_noise_frames = []
noise_mag_avg = np.zeros(framedata_n["frame_size"])
for i in range(len(noise_frames)):
    noise_frames[i] = noise_frames[i] * ham
    noise_frames[i] = np.fft.fft(noise_frames[i])
    noise_mag_avg += np.abs(noise_frames[i])
noise_mag_avg /= len(noise_frames)


# noise subtraction
frame_mag_estimate = []
for i in range(len(frame_mag)):
    frame_mag_estimate.append((frame_mag[i] - noise_mag_avg).astype('complex128'))
    # avoid negative magnitude 
    for j in range(frame_mag_estimate[i].size):
        if(frame_mag_estimate[i][j] <= 0.01 * noise_mag_avg[j]):
            frame_mag_estimate[i][j] = 0.01 * noise_mag_avg[j]

 


#%%

# phase correction
for i in range(len(frame_mag_estimate)):
    frame_mag_estimate[i] *= np.exp(1.0j* frame_angle[i])
    frame_mag_estimate[i] = np.fft.ifft(frame_mag_estimate[i]).real

#%%

# reconstuction
ad.ola_and_write(framedata["data_size"], framedata["hop_size"], frame_mag_estimate, "lecture_spec.wav", framedata["sample_rate"], framedata["frame_size"])




# %%
