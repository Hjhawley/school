#!/usr/bin/env python3

import os
import librosa
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# === CONFIG ===
SAMPLE_RATE = 44100  # Audio sample rate (standard CD quality)
N_FFT = 1024         # FFT window size for STFT
HOP_LENGTH = 256     # Hop length for STFT (overlap control)
WIN_LENGTH = 1024    # Window length for STFT
CLIP_DURATION = 5    # Duration of each audio clip in seconds


def load_audio_pair(path_degraded, path_clean):
    """
    Load a pair of audio files (degraded and clean),
    compute their spectrograms, convert to log scale,
    normalize, and return as float32 tensors with shape (freq, time, 1)
    """
    # Load audio files and resample to the target sample rate, convert to mono
    y_deg, _ = librosa.load(path_degraded, sr=SAMPLE_RATE, mono=True)
    y_cln, _ = librosa.load(path_clean, sr=SAMPLE_RATE, mono=True)

    # Compute magnitude spectrograms via STFT
    S_deg = np.abs(librosa.stft(y_deg, n_fft=N_FFT, hop_length=HOP_LENGTH, win_length=WIN_LENGTH))
    S_cln = np.abs(librosa.stft(y_cln, n_fft=N_FFT, hop_length=HOP_LENGTH, win_length=WIN_LENGTH))

    # Convert amplitude to log-decibel scale for better perceptual modeling
    log_deg = librosa.amplitude_to_db(S_deg, ref=np.max)
    log_cln = librosa.amplitude_to_db(S_cln, ref=np.max)

    # Normalize values to range [0, 1] to help the neural network train more stably
    norm_deg = (log_deg + 80) / 80  # Assumes dB values fall in [-80, 0]
    norm_cln = (log_cln + 80) / 80

    # Add channel dimension to match expected model input: (freq, time, 1)
    norm_deg = norm_deg[..., np.newaxis].astype(np.float32)
    norm_cln = norm_cln[..., np.newaxis].astype(np.float32)

    return norm_deg, norm_cln


def load_dataset(degraded_dir, clean_dir):
    """
    Load and preprocess all matching pairs of degraded/clean audio files.
    Returns two numpy arrays: X (inputs), y (targets).
    """
    X = []
    y = []

    # Load all filenames from the degraded directory
    filenames = sorted(f for f in os.listdir(degraded_dir) if f.endswith(".wav"))
    for fname in filenames:
        path_deg = os.path.join(degraded_dir, fname)
        path_cln = os.path.join(clean_dir, fname)

        # Skip files that are missing their matching pair
        if not os.path.exists(path_cln):
            print(f"Skipping {fname}: no matching clean file")
            continue

        # Load and preprocess the pair
        spec_deg, spec_cln = load_audio_pair(path_deg, path_cln)
        X.append(spec_deg)
        y.append(spec_cln)

    # Convert list of arrays to single stacked numpy arrays
    X = np.array(X)
    y = np.array(y)
    print(f"Loaded {len(X)} samples. Input shape: {X[0].shape}")
    return X, y


def get_datasets(X, y, val_split=0.15, batch_size=8):
    """
    Split the dataset into training and validation sets,
    and return them as TensorFlow data pipelines.
    """
    # Split the full dataset into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=val_split, random_state=42)

    # Wrap in tf.data.Dataset objects
    train_ds = tf.data.Dataset.from_tensor_slices((X_train, y_train))
    val_ds = tf.data.Dataset.from_tensor_slices((X_val, y_val))

    # Shuffle and batch the training set; just batch the validation set
    train_ds = train_ds.shuffle(1000).batch(batch_size).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)

    return train_ds, val_ds
