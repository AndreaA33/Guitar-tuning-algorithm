import sounddevice  as sd
import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import pandas as pd

def record():
    fs = 44100
    duration = 5
    myrecording = sd.rec(duration *fs, samplerate = fs, channels = 2, dtype = "float32")
    print("recording")
    sd.wait()
    print("complete")
    sd.play(myrecording, fs)
    sd.wait()
    print("finished recording")

    # Frequency / pitch of the sine wave
    freq_hz = 440.0

    waveform = np.sin(2 * np.pi * myrecording * freq_hz / fs)
    waveform_quiet = waveform * 5
    waveform_integers = np.int16(waveform_quiet * 32767)


    # Write the .wav file
    write('first_sine_wave4.wav', fs, waveform_integers)

# record()

def comparison(recording1,recording2):
    dframe = pd.DataFrame(recording1)
    return dframe

samplerate1, data1 = wavfile.read("first_sine_wave.wav")
samplerate2, data2 = wavfile.read("first_sine_wave2.wav")
comparison(data1.shape[0],data2.shape[0])

print(f"number of channels = {data1.shape[0]}")



 