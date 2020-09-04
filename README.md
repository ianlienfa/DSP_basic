# Audio Processing

Created: Sep 3, 2020 2:54 PM

### 前言

這個暑假跟康明軒老師還有幾個同學一起研究跟音訊處理相關的題目
我們包含老師都沒有什麼類似的經驗，不過都對這個主題頗有興趣，加上音訊處理會用到蠻多關於傅立葉轉換等等的數學工具，所以老師在這方面還能處理，於是就開始了我們的小小研究。

## Fourier Transform

Transformation plays an important part of digital signal processing(DSP), and the most famous transform is Fourier Transform, in short, Fourier Transform allows us to interpret a signal into many different sin, cos waves, which make it easy to do further adjustment.

# Implemented Signal Effects

---

## → Time Stretching

Link to code: [https://github.com/ianlienfa/DSP_basic/blob/master/time_stretching.py](https://github.com/ianlienfa/DSP_basic/blob/master/time_stretching.py)

**How we save sound files in computer:**

We know that sound wave is continuous, but computers only save discrete data.
So we set up a rate of sampling frequency, which is *sample rate*, and only save the value at specific time span

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled.png)

We only save the value of blue points

With that in mind, stretching sound file is quite easy, all we have to do is change the sample rate, right?
If we want it sound slower, simply set the sample rate larger, and vice versa.

Well, it's not that simple, observe Diagram 1.1, if we set the sample rate twice as the original sample rate, our computer will see these blue point be captured in a half second, but the frequency of it will also be doubled, resulting in the change of the pitch.

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%201.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%201.png)

Diagram 1.1

**Use SOLA algorithm to preserve the pitch**

To fix this problem, we use a SOLA(Synchronous overlap and add) algorithm to retain the frequency. SOLA works as follows:

1. Sample the sound file in a chosen length

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%202.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%202.png)

2. Reposition the blocks 

3. Move forwards or backwards slightly to find the optimal match for overlapping signals
(optimal match is the position with largest cross-correlation) ← The hardest part

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%203.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%203.png)

4. fade in and fade out at the overlapping part         

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%204.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%204.png)

Using this procedure, we can stretch the time of a sound file while retaining its pitch and frequency.

note that we didn't change the sample rate using this procedure:

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%205.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%205.png)

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%206.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%206.png)

Observe that the second wave is 2 times longer then the first one

Original File

[Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/s440.wav](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/s440.wav)

Double Stretched File

[Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/s440_x.5.wav](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/s440_x.5.wav)

```python
#%%
import scipy.io.wavfile as wv
import numpy as np
import matplotlib.pyplot as plt
import audiolib as ad

# %%
semitones = 2
(framedata, data) = ad.read_in_and_framing_r('s440.wav', 1760, 0.8)
scale_audio = ad.scale_audio(2, framedata, data)

# %%
wv.write("s440_x.5.wav", framedata["sample_rate"], scale_audio)
```

# → Pitch Shifting

Link to code: [https://github.com/ianlienfa/DSP_basic/blob/master/pitch_shifting.py](https://github.com/ianlienfa/DSP_basic/blob/master/pitch_shifting.py)

There are many ways to achive pitch shifting, here we use a quite simple procedure based on SOLA:

Recall that we can stretch signal by changing the sample rate, but will also affect the frequency:

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%201.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%201.png)

Diagram 1.1

The idea of shifting the pitch is simple, take doubling the frequency for example, 
first, sqeeze the sound wave and make the length of it become half with double frequency, 
then, do the time stretching to recover the length while retaining the frequency

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%207.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%207.png)

Diagram 2.1

Notice that from step 1 to 2, the procedure is not *changing the sample rate* like metioned above but *Resampling*

This is because we usually hope to keep the sample rate stable.

**Resampling** 

Resampling is the way to shrink or to expand the signal, this procedure changes the frequency

For signal array with index [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:

To shrink it by half, sample the data with index[0, 2, 4, 6, 8]

To shrink it by 1/3, sample the data with index[0, 3, 6, 9]

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%208.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%208.png)

To expand it, interpolation can be used.

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%209.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%209.png)

```python
import scipy.io.wavfile as wv
import numpy as np
import matplotlib.pyplot as plt
import audiolib as ad

# %%

semitones = 2
(framedata, data) = ad.read_in_and_framing_r('s440.wav', 1760, 0.8)
scale_audio = ad.scale_audio(2, framedata, data)
scale_audio = ad.speedx(scale_audio, 2)  # <- the only different is after stretching we do resampling

# %%
wv.write("s440_x.5.wav", framedata["sample_rate"], scale_audio)
```

Original File

[Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/s440%201.wav](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/s440%201.wav)

An Octave higher (2x frequency)

[Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/s440_high_2.wav](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/s440_high_2.wav)

# → Noise Reduction — using spectral subtraction

Link to code: [https://github.com/ianlienfa/DSP_basic/blob/master/spectral_rdc.py](https://github.com/ianlienfa/DSP_basic/blob/master/spectral_rdc.py)

There're also tons of ways to reduce the noise inside a sound file,one of the often used technique is called spectral subtraction

Spectral Subtraction Requires two input, the noisy sound file and the noise segment file.
The way it subtract noise from the signal is to analyse the frequency spectral of the noise file and lower the relative frequency of the noisy sound file.

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%2010.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%2010.png)

To Analyse the frequency Spectral of a signal, we make use of the priorly mentioned *Fourier Transform.*

More precisely, the transform using here is *Discrete-Time Fourier Transform*, it actually has great difference with *Fourier Transform* in the implementation aspect, but we only want the idea of Transformation here.

Before reduction (Notice the existing background noise)

[Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/noisy.wav](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/noisy.wav)

After reduction

[Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/noisy_rdc.wav](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/noisy_rdc.wav)

Though producing clear sound, this method is quite costy, with it needing one extra "noise sound file."
To gain more flexibility, here's another method.

# → Noise Reduction — using Wavelet Transform

Link to code: [https://github.com/ianlienfa/DSP_basic/blob/master/wavelet_rdc.py](https://github.com/ianlienfa/DSP_basic/blob/master/wavelet_rdc.py)

There are many kinds of transformation to make it easier to make adjustments on signals, the most common one is Fourier Transform, which interprets a signal into many sin and cos waves. There exists another fashion, which interprets signal into many "wavelets".

The object of descibing signal using wavelets is to "roughly" depict the sound wave using wavelet, when we abandon some small details leading to noises, the sound becomes clearer.

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%2011.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%2011.png)

![Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%2012.png](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/Untitled%2012.png)

observe the above diagram, we can see that by "roughly" describing the signal, we can make the sound wave smoother and clearer.

The good thing about this algorithm is that we no longer need the extra noise file but only the original noisy file. However, this methods needs to be adjust for different kinds of scenario, since there exists tons of different wavelets, some wavelets suit human-speaking voices, some suit instrument sound waves. What's more, in my experience, this method is better at denoising abrupt and sudden noises instead of persistent background noise like spetral subtraction, so using both method on the noise is recommanded.

Sound File After Spectral Subtraction (Notice the high frequency noise)

[Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/lecture_spec.wav](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/lecture_spec.wav)

Sound File After Wavelet Trasform Denoising

[Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/lecture_wavlet.wav](Audio%20Processing%204cc756f8304140b4a3f0a1cecbf17d21/lecture_wavlet.wav)

References:

- **DAFX: Digital Audio Effects, Second Edition,** by Udo Zölzer
- **The Scientist and Engineer's Guide toDigital Signal Processing,** by Steven W. Smith, Ph.D.
- Stephan Bernsee's Blog, [http://blogs.zynaptiq.com/bernsee/](http://blogs.zynaptiq.com/bernsee/)
- Guitar Pitch Shifter, [http://www.guitarpitchshifter.com/algorithm.html#33](http://www.guitarpitchshifter.com/algorithm.html#33)
- **A Tutorial of the Wavelet Transform,** by ****Chun-Lin, Liu
- **Speech denoising using discrete wavelet packet decomposition technique,** by Oktar, Mehmet Alper ; Nibouche, Mokhtar ; Baltaci, Yusuf