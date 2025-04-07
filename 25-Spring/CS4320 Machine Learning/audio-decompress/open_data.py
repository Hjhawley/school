#!/usr/bin/env python3

import os
import librosa
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# === CONFIG ===
SAMPLE_RATE = 44100
N_FFT = 1024
HOP_LENGTH = 256
WIN_LENGTH = 1024
CLIP_DURATION = 5  # seconds


def load_audio_pair(path_degraded, path_clean):
    # Load audio files
    y_deg, _ = librosa.load(path_degraded, sr=SAMPLE_RATE, mono=True)
    y_cln, _ = librosa.load(path_clean, sr=SAMPLE_RATE, mono=True)

    # Compute magnitude spectrograms
    S_deg = np.abs(librosa.stft(y_deg, n_fft=N_FFT, hop_length=HOP_LENGTH, win_length=WIN_LENGTH))
    S_cln = np.abs(librosa.stft(y_cln, n_fft=N_FFT, hop_length=HOP_LENGTH, win_length=WIN_LENGTH))

    # Convert to log scale (decibels)
    log_deg = librosa.amplitude_to_db(S_deg, ref=np.max)
    log_cln = librosa.amplitude_to_db(S_cln, ref=np.max)

    # Normalize to [0, 1] for model stability
    norm_deg = (log_deg + 80) / 80  # assuming log_db range ~[-80, 0]
    norm_cln = (log_cln + 80) / 80

    # Add channel dimension for TensorFlow (freq, time, 1)
    norm_deg = norm_deg[..., np.newaxis].astype(np.float32)
    norm_cln = norm_cln[..., np.newaxis].astype(np.float32)

    return norm_deg, norm_cln


def load_dataset(degraded_dir, clean_dir):
    X = []
    y = []
    
    filenames = sorted(f for f in os.listdir(degraded_dir) if f.endswith(".wav"))
    for fname in filenames:
        path_deg = os.path.join(degraded_dir, fname)
        path_cln = os.path.join(clean_dir, fname)
        if not os.path.exists(path_cln):
            print(f"Skipping {fname}: no matching clean file")
            continue

        spec_deg, spec_cln = load_audio_pair(path_deg, path_cln)
        X.append(spec_deg)
        y.append(spec_cln)

    X = np.array(X)
    y = np.array(y)
    print(f"Loaded {len(X)} samples. Input shape: {X[0].shape}")
    return X, y


def get_datasets(X, y, val_split=0.15, batch_size=8):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=val_split, random_state=42)

    train_ds = tf.data.Dataset.from_tensor_slices((X_train, y_train))
    val_ds = tf.data.Dataset.from_tensor_slices((X_val, y_val))

    train_ds = train_ds.shuffle(1000).batch(batch_size).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)

    return train_ds, val_ds
