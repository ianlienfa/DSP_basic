#%%
import scipy.io.wavfile as wv
import numpy as np
import matplotlib.pyplot as plt
import audiolib as ad


# %%

semitones = 2
(framedata, data) = ad.read_in_and_framing_r('s440.wav', 1760, 0.8)
scale_audio = ad.scale_audio(2, framedata, data)    # SOLA implemented


# %%
wv.write("s440_x.5.wav", framedata["sample_rate"], scale_audio)


# %%