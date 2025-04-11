import librosa
import numpy as np
import tensorflow as tf
import soundfile as sf
import subprocess

def preprocess_audio(path):
    y, _ = librosa.load(path, sr=44100, mono=True)
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=256, win_length=1024))
    log_S = librosa.amplitude_to_db(S, ref=np.max)
    norm_S = (log_S + 80) / 80
    return norm_S[np.newaxis, ..., np.newaxis].astype(np.float32)  # shape (1, 513, N, 1)

def postprocess_spectrogram(spectrogram):
    db = spectrogram.squeeze() * 80 - 80
    mag = librosa.db_to_amplitude(db)
    y = librosa.griffinlim(mag, n_fft=1024, hop_length=256, win_length=1024)
    return y

def restore_audio(input_mp3, output_mp3, model_path="models/audio_decompressor_latest.keras"):
    print("Loading model...")
    model = tf.keras.models.load_model(model_path)

    print("Preprocessing audio...")
    input_spec = preprocess_audio(input_mp3)

    print("Running inference...")
    output_spec = model.predict(input_spec)

    print("Reconstructing waveform...")
    y = postprocess_spectrogram(output_spec)

    print("Saving intermediate WAV...")
    sf.write("temp_output.wav", y, 44100)

    print("Converting to MP3...")
    subprocess.run(["ffmpeg", "-y", "-i", "temp_output.wav", "-b:a", "320k", output_mp3])

    print(f"Restored MP3 saved to {output_mp3}")
