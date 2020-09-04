#%%
import scipy.io.wavfile as wv
import numpy as np
import matplotlib.pyplot as plt
import math


def coeff_limit(L1, L2):
    r_l1l2 = np.empty(0)

    for m in range (max(int(L1.size * 0.1), 40)):
        ll1 = L1[m:]
        ll2 = L2[:(L1.size - m)]
        l = np.ma.corrcoef(np.array([ll1, ll2]))
        r_l1l2 = np.append(r_l1l2, l[0][1])

    max_val = 0
    max_index = 0
    for i in range(r_l1l2.size):
        if(r_l1l2[i] > max_val):
            max_val = r_l1l2[i]
            max_index = i

    return max_index, max_val    


def read_in_and_framing_r(filename, point_per_frame, overlap_ratio):
    # readin
    (sr, data) = wv.read(filename)
    
    # some basic framing parameters, no overlap, about 20ms a time, that is about 1024 point a frame
    overlap = int(point_per_frame * overlap_ratio)
    hop_size = point_per_frame - overlap
    # print('hopsize:', hop_size)
    # print('datasize:', data.size)

    # deciding frame count
    less = data.size % hop_size
    if(less == 0):
        frame_ct = int(data.size / hop_size)
    else:
        if(less <= point_per_frame - hop_size):            
            frame_ct = int(data.size / hop_size)
        else:
            frame_ct = int(data.size / hop_size) + 1

    frames = []
    start = 0
    end = point_per_frame

    # framing 
    for x in range(frame_ct):
        frames.append(data[start: end])
        start += hop_size
        end += hop_size
    
    # check if exists dummy frames
    is_last = False  
    frame_ct_temp = frame_ct
    for i in range(frame_ct_temp):
        if(is_last):
            # then the frame still exists are dummy frames
            frames = frames[:i]
            frame_ct = i
            break
        else:
            if(frames[i].size != point_per_frame):
                is_last = True

    # framedata
    framedata = {
        "data":data,
        "datasize": data.size,
        "framesize": point_per_frame,
        "sample_rate": sr,
        "overlap_points_ct": overlap,
        "frame_ct":frame_ct,
        "hopsize":hop_size
    }

    # return original file data size, sample rate, and the frames
    return framedata, frames


def scale_audio(alpha, framedata, data):
    framesize = framedata["framesize"]
    Sa = framedata["hopsize"]
    overlap = framedata["overlap_points_ct"]
    datasize = framedata["datasize"]
    frames = []
    for i in range(framedata["frame_ct"]):
        frames.append(np.copy(data[i]))

    # M is frame_count
    M = framedata["frame_ct"]

    # 真正伸展長度應該是
    # scale_effect ~= alpha * Sa * M + overlap * (M - 1) + 調整參數
    # synthesis step : 1. some process before adding up
    # add_at is an array saving the index should the n1 be at to add up n2
    Ss = int(alpha * Sa)
    new_overlap = framesize - Ss
    add_at = np.empty(M)
    for i in range(add_at.size):
        add_at[i] = i * Ss

    # 用一個個黏的
    scale_audio = frames[0]

    for n in range(0, M-1):

        new_scale_size = Ss * (n+1)
        n1 = scale_audio[new_scale_size+1 :]
        n2 = frames[n+1][: n1.size]

        if(n2.size < n1.size):
            n1 = scale_audio[scale_audio.size - n2.size:]

        # calculate the cross correlation
        (max_index, max_val) = coeff_limit(n1, n2)

        # left = frames[n][:Ss+max_index]
        tt = new_scale_size+1+max_index 
        new_n1 = n1[max_index :]
        new_n2 = frames[n+1][: new_n1.size]
        right = frames[n+1][new_n1.size:]

        fade_out = np.linspace(1, 0, new_n1.size)
        fade_in = np.linspace(0, 1, new_n2.size)

        # new_n1 = new_n1 * fade_out

        new_n1 = new_n1 * fade_out
        new_n2 = new_n2 * fade_in

        overlapping_part = new_n1 + new_n2
        scale_audio[scale_audio.size - overlapping_part.size: ] = overlapping_part
        scale_audio = np.append(scale_audio, right)

        scale_audio = scale_audio.real.astype('int16')

    return scale_audio


def speedx(sound_array, factor):
    indices = np.round( np.arange(0, sound_array.size, factor) )
    indices = indices[indices < sound_array.size].astype(int)
    new_array = np.empty(0)
    for i in range(indices.size):
        if(indices[i] < sound_array.size):
            new_array = np.append(new_array, sound_array[indices[i]])
    return new_array.astype('int16')
        

def loadfile_and_frame(filename, point_per_frame, overlap_ratio):
    # readin
    (sr, data) = wv.read(filename)
    
    # some basic framing parameters, no overlap, about 20ms a time, that is about 1024 point a frame
    overlap = int(point_per_frame * overlap_ratio)
    hop_size = point_per_frame - overlap
    # print('hopsize:', hop_size)
    # print('datasize:', data.size)

    # deciding frame count

    frame_ct = math.ceil((data.size - point_per_frame)/hop_size + 1) 
    frames = []
    start = 0
    end = point_per_frame

    # framing 
    for x in range(frame_ct):
        temp = np.zeros(point_per_frame)
        points = data[start: end]
        temp[0: points.size] = points
        frames.append(temp)
        start += hop_size
        end += hop_size

    
    # framedata
    framedata = {
        "data":data,
        "data_size": data.size,
        "frame_size": point_per_frame,
        "sample_rate": sr,
        "overlap_points_ct": overlap,
        "frame_ct":frame_ct,
        "hop_size":hop_size
    }

    # return original file data size, sample rate, and the frames
    return framedata, frames


def ola_and_write(output_size, hop, frames, write_file_name, sample_rate, frame_size):
    output_arr = np.zeros(output_size)
    start = 0
    for i in range(len(frames)):
        add = frames[i][0 : output_arr[start: start+frame_size].size]
        output_arr[start: start+frame_size] += add
        start += hop

    output_arr = (output_arr/2).astype('int16')

    wv.write(write_file_name, sample_rate, output_arr)

