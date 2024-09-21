import wave 
import sounddevice  as sd
from scipy.io.wavfile import write
import sys 
import matplotlib.pyplot as plt
import numpy as np
from numpy import diff, argmax
from mpl_interactions import ioff, panhandler, zoom_factory

def autocorrelation(x,fs):
    result = np.correlate(x, x, mode='full')

    result = result[len(result)//2:]

    d = diff(result)
    start = np.where(d > 0)[0][0]

    peak = argmax(result[start:]) + start
    px, py = parabolic(result, peak)

    frequency = fs / px
    
    return result, frequency

def parabolic(f, x):

    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)

def bounds(f):

    notes = [["E", 82],["A", 111],["D", 146,],["G", 196],["B", 246],["E", 330]]

    for i in range(1, len(notes)):
        if i+1 < len(notes):
            if f == notes[i][1]:
                print(f"{notes[i][0]} is tuned")
            elif f > notes[i-1][1] and f < notes[i][1]:
                print(f"{notes[i][0]} -------- {f:.2f} -------- {notes[i+1][0]}")


def plot_wav_with_autocorrelation(filename):
    # Open the WAV file
    with wave.open(filename, "r") as spf:
        # Check if it's a mono file
        if spf.getnchannels() != 1:
            print("Error: This script only works for mono WAV files.")
            sys.exit(1)
        
        # Get file parameters
        fs = spf.getframerate()
        n_frames = spf.getnframes()
        
        # Extract Raw Audio from Wav File
        signal = spf.readframes(n_frames)
        signal = np.frombuffer(signal, dtype=np.int16)
        
        # Convert to float32 and normalize
        signal = signal.astype(np.float32) / np.iinfo(np.int16).max

    # Create time array
    duration = n_frames / fs
    time = np.linspace(0, duration, num=n_frames)

    # Calculate autocorrelation
    autocorr, frequency = autocorrelation(signal,fs)
    autocorr_time = np.linspace(0, duration, num=len(autocorr))

    bounds(frequency)

# Use the function

def record():
    fs = 44100
    duration = 1
    while True:
        myrecording = sd.rec(duration * fs, samplerate = fs, channels = 1, dtype = "float32")
        print("recording")
        sd.wait()
        print("complete")
        print("finished recording")

        # Frequency / pitch of the sine wave
        freq_hz = 440.0

        waveform = np.sin(2 * np.pi * myrecording * freq_hz / fs)
        waveform_quiet = waveform * 10
        waveform_integers = np.int16(waveform_quiet * 32767)


        # Write the .wav file
        write('Sound.wav', fs, waveform_integers)
        plot_wav_with_autocorrelation("Sound.wav")


record()
