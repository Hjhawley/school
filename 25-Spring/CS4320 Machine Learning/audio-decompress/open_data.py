import os
import librosa
import numpy as np
import tensorflow as tf

# config
SAMPLE_RATE = 44100  # Audio sample rate (standard CD quality)
N_FFT = 1024         # FFT window size for Short-Time Fourier Transform (STFT)
HOP_LENGTH = 256     # Hop length for STFT (overlap control)
WIN_LENGTH = 1024    # Window length for STFT


def load_audio_pair(path_degraded, path_clean):
    y_deg, _ = librosa.load(path_degraded, sr=SAMPLE_RATE, mono=True)
    y_cln, _ = librosa.load(path_clean, sr=SAMPLE_RATE, mono=True)

    S_deg = np.abs(librosa.stft(y_deg, n_fft=N_FFT, hop_length=HOP_LENGTH, win_length=WIN_LENGTH))
    S_cln = np.abs(librosa.stft(y_cln, n_fft=N_FFT, hop_length=HOP_LENGTH, win_length=WIN_LENGTH))

    log_deg = librosa.amplitude_to_db(S_deg, ref=np.max)
    log_cln = librosa.amplitude_to_db(S_cln, ref=np.max)

    norm_deg = (log_deg + 80) / 80
    norm_cln = (log_cln + 80) / 80

    norm_deg = norm_deg[..., np.newaxis].astype(np.float32)
    norm_cln = norm_cln[..., np.newaxis].astype(np.float32)

    return norm_deg, norm_cln


def audio_pair_generator(degraded_dir, clean_dir):
    filenames = sorted(f for f in os.listdir(degraded_dir) if f.endswith(".wav"))
    for fname in filenames:
        path_deg = os.path.join(degraded_dir, fname)
        path_cln = os.path.join(clean_dir, fname)
        if not os.path.exists(path_cln):
            print(f"Missing clean file for {fname}, skipping.")
            continue
        try:
            yield load_audio_pair(path_deg, path_cln)
        except Exception as e:
            print(f"Error loading {fname}: {e}, skipping.")


def get_streaming_dataset(degraded_dir, clean_dir, batch_size=8, shuffle_buffer=500):
    sample_shape = (513, 862, 1)

    dataset = tf.data.Dataset.from_generator(
        lambda: audio_pair_generator(degraded_dir, clean_dir),
        output_signature=(
            tf.TensorSpec(shape=sample_shape, dtype=tf.float32),
            tf.TensorSpec(shape=sample_shape, dtype=tf.float32),
        )
    )

    return dataset.shuffle(shuffle_buffer).batch(batch_size).prefetch(tf.data.AUTOTUNE)


# Test the generator with a batch
if __name__ == "__main__":
    train_ds = get_streaming_dataset("data/train/cut/degraded", "data/train/cut/clean")
    for X_batch, y_batch in train_ds.take(1):
        print("X_batch shape:", X_batch.shape)
        print("y_batch shape:", y_batch.shape)
