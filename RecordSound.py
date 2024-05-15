import sounddevice  as sd
import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

fs = 44100
duration = 5
myrecording = sd.rec(duration *fs, samplerate = fs, channels = 2, dtype = "float32")
print("recording")
sd.wait()
print("complete")
sd.play(myrecording, fs)
sd.wait()
print("finished playing")




# Frequency / pitch of the sine wave
freq_hz = 440.0

# NumpPy magic
waveform = np.sin(2 * np.pi * myrecording * freq_hz / fs)
waveform_quiet = waveform * 2
waveform_integers = np.int16(waveform_quiet * 32767)

# Write the .wav file
write('first_sine_wave2.wav', fs, waveform_integers)

samplerate, data = wavfile.read("first_sine_wave.wav")
print(f"number of channels = {data.shape[0]}")

