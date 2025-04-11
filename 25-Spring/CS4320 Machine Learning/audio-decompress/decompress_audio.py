import os
import numpy as np
import librosa
import soundfile as sf
import tensorflow as tf
import subprocess
from scipy.signal.windows import hann

SAMPLE_RATE = 44100
WINDOW_DURATION = 5.0
WINDOW_STRIDE = 2.5
N_FFT = 1024
HOP_LENGTH = 256
WIN_LENGTH = 1024

def preprocess_audio(y):
    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH, win_length=WIN_LENGTH))
    log_S = librosa.amplitude_to_db(S, ref=np.max)
    norm_S = (log_S + 80) / 80
    return norm_S.astype(np.float32)[..., np.newaxis]  # (513, T, 1)

def postprocess_spectrogram(mag_spec):
    db = mag_spec * 80 - 80
    mag = librosa.db_to_amplitude(db)
    return librosa.griffinlim(mag, n_fft=N_FFT, hop_length=HOP_LENGTH, win_length=WIN_LENGTH)

def restore_audio(input_path, output_path, model_path="models/audio_decompressor_latest.keras"):
    print("Loading model...")
    model = tf.keras.models.load_model(model_path)

    print("Loading audio...")
    y, _ = librosa.load(input_path, sr=SAMPLE_RATE, mono=True)
    total_samples = len(y)
    window_size = int(WINDOW_DURATION * SAMPLE_RATE)
    stride_size = int(WINDOW_STRIDE * SAMPLE_RATE)
    
    output = np.zeros(total_samples)
    weight = np.zeros(total_samples)
    hann_window = hann(window_size, sym=False)

    print("Processing in sliding windows...")
    for start in range(0, total_samples - window_size + 1, stride_size):
        chunk = y[start:start + window_size]
        input_spec = preprocess_audio(chunk)
        input_spec = np.expand_dims(input_spec, axis=0)  # (1, 513, T, 1)

        output_spec = model.predict(input_spec)[0]  # (513, T, 1)
        y_hat = postprocess_spectrogram(output_spec.squeeze())

        # Overlap-add using Hann window
        y_hat = y_hat[:window_size]  # trim if needed
        output[start:start + window_size] += y_hat * hann_window
        weight[start:start + window_size] += hann_window

    print("Finalizing audio...")
    weight[weight == 0] = 1e-8  # avoid division by zero
    output /= weight

    print("Saving WAV...")
    sf.write("temp_output.wav", output, SAMPLE_RATE)

    print("Converting to MP3...")
    subprocess.run(["ffmpeg", "-y", "-i", "temp_output.wav", "-b:a", "320k", output_path])

    print(f"Done! Restored MP3 saved to {output_path}")
