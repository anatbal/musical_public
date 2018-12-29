"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys

from pyaudio import PyAudio, paContinue, paFloat32, paInt16
from time import sleep
import numpy as np
from numpy import array, random, arange, float32, float64, zeros, int16
import matplotlib.pyplot as plt

import pyaudio, sys
from wavefile import WaveReader


################################### Constants ##################################

fs            = 44100   # Hz
threshold     = 0.8     # absolute gain
delay         = 40      # samples
signal_length = 1       # second
release_coeff = 0.9999  # release time factor
attack_coeff  = 0.9     # attack time factor
dtype         = float32 # default data type
block_length  = 1024    # samples

############################# Implementation of Limiter ########################

class Limiter:
    def __init__(self, attack_coeff, release_coeff, delay, dtype=float32):
        self.delay_index = 0
        self.envelope = 0
        self.gain = 1
        self.delay = delay
        self.delay_line = zeros(delay, dtype=dtype)
        self.release_coeff = release_coeff
        self.attack_coeff = attack_coeff

    def limit(self, signal, threshold):
        for i in arange(len(signal)):
            self.delay_line[self.delay_index] = signal[i]
            self.delay_index = (self.delay_index + 1) % self.delay

            # calculate an envelope of the signal
            self.envelope *= self.release_coeff
            self.envelope  = max(abs(signal[i]), self.envelope)

            # have self.gain go towards a desired limiter gain
            if self.envelope > threshold:
                target_gain = (1+threshold-self.envelope)
            else:
                target_gain = 1.0
            self.gain = ( self.gain*self.attack_coeff +
                          target_gain*(1-self.attack_coeff) )

            # limit the delayed signal
            signal[i] = self.delay_line[self.delay_index] * self.gain
            
            
            
if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = WaveReader(sys.argv[1])
#wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

limiter = Limiter(attack_coeff, release_coeff, delay, dtype)

def callback(in_data, frame_count, time_info, flag):
    if flag:
        print("Playback Error: %i" % flag)
    data = np.zeros((1,block_length), np.float32, order='F')

    nframes = wf.read(data)
    played_frames = callback.counter
    callback.counter += nframes
    a = array(data[0,:])
    limiter.limit(a, threshold)
    return a, paContinue

callback.counter = 0

# define callback (2)
# def callback(in_data, frame_count, time_info, status):
    # data = wf.readframes(frame_count)
    # return (data, pyaudio.paContinue)

    # open stream using callback (3)
stream = p.open(format=paFloat32,
                channels=1,
                rate=fs,
                frames_per_buffer = block_length,
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    time.sleep(0.1)

# stop stream (6)
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio (7)
p.terminate()

