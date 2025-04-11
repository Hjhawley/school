import os
import numpy as np
import librosa
import soundfile as sf
import tensorflow as tf
import subprocess
import argparse
from scipy.signal.windows import hann

# config
SAMPLE_RATE = 44100
WINDOW_DURATION = 5.0     # seconds
WINDOW_STRIDE = 2.5       # seconds
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

def restore_audio(input_path, output_path, model_path):
    print("Loading model...")
    model = tf.keras.models.load_model(model_path)

    print("Loading input audio...")
    y, _ = librosa.load(input_path, sr=SAMPLE_RATE, mono=True)
    total_samples = len(y)
    window_size = int(WINDOW_DURATION * SAMPLE_RATE)
    stride_size = int(WINDOW_STRIDE * SAMPLE_RATE)
    
    output = np.zeros(total_samples)
    weight = np.zeros(total_samples)
    hann_window = hann(window_size, sym=False)

    print("Running inference with sliding window...")
    for start in range(0, total_samples - window_size + 1, stride_size):
        chunk = y[start:start + window_size]
        input_spec = preprocess_audio(chunk)
        input_spec = np.expand_dims(input_spec, axis=0)  # (1, 513, T, 1)

        output_spec = model.predict(input_spec)[0]  # (513, T, 1)
        y_hat = postprocess_spectrogram(output_spec.squeeze())

        y_hat = y_hat[:window_size]  # clip in case of overshoot
        output[start:start + window_size] += y_hat * hann_window
        weight[start:start + window_size] += hann_window

    print("Normalizing and finalizing output...")
    weight[weight == 0] = 1e-8
    output /= weight

    print("Saving intermediate WAV...")
    temp_wav = "temp_output.wav"
    sf.write(temp_wav, output, SAMPLE_RATE)

    print("Converting to MP3...")
    subprocess.run(["ffmpeg", "-y", "-i", temp_wav, "-b:a", "320k", output_path])

    print(f"Restored MP3 saved to: {output_path}")
    os.remove(temp_wav)

def main():
    parser = argparse.ArgumentParser(description="Restore audio using a trained spectrogram model.")
    parser.add_argument("input", help="Path to input MP3 file")
    parser.add_argument("output", help="Path to output MP3 file")
    parser.add_argument("--model", default="models/audio_decompressor_latest.keras", help="Path to trained Keras model")

    args = parser.parse_args()
    restore_audio(args.input, args.output, args.model)

if __name__ == "__main__":
    main()
