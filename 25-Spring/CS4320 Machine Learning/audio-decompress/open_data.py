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
        print(f"Processing {fname}")  # <-- sanity check
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


def get_static_batch_dataset(degraded_dir, clean_dir, batch_size=8, skip=0):
    """
    Loads a static batch of audio pairs into memory for evaluation.

    Args:
        degraded_dir (str): Path to degraded audio files.
        clean_dir (str): Path to clean audio files.
        batch_size (int): Number of samples to return.
        skip (int): Number of files to skip before starting (useful for testing different chunks).

    Returns:
        Tuple of (X_batch, y_batch) as numpy arrays.
    """
    generator = audio_pair_generator(degraded_dir, clean_dir)
    
    # Skip first N files if needed
    for _ in range(skip):
        try:
            next(generator)
        except StopIteration:
            raise ValueError("Skip value exceeds available files.")

    X_batch, y_batch = [], []
    
    for _ in range(batch_size):
        try:
            x, y = next(generator)
            X_batch.append(x)
            y_batch.append(y)
        except StopIteration:
            break

    if not X_batch:
        raise ValueError("No data loaded. Check directories and skip/batch_size values.")

    return np.stack(X_batch), np.stack(y_batch)


# Test the generator with a batch and save PNGs of the first sample
if __name__ == "__main__":
    train_ds = get_streaming_dataset("data/train/cut/degraded", "data/train/cut/clean")

    for i, (X_batch, y_batch) in enumerate(train_ds.take(1)):
        print("X_batch shape:", X_batch.shape)
        print("y_batch shape:", y_batch.shape)

        degraded = X_batch[0].numpy().squeeze()
        clean = y_batch[0].numpy().squeeze()

        import matplotlib.pyplot as plt
        import librosa.display

        # Calculate time axis in seconds
        num_frames = degraded.shape[1]
        times = librosa.frames_to_time(np.arange(num_frames), sr=SAMPLE_RATE, hop_length=HOP_LENGTH)

        # Degraded Spectrogram
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(degraded, sr=SAMPLE_RATE, hop_length=HOP_LENGTH,
                                 x_axis='time', y_axis='linear', cmap='viridis')
        plt.title("Degraded Spectrogram (Sample 0)")
        plt.colorbar(label="Normalized dB")
        plt.tight_layout()
        plt.savefig("degraded_sample_0.png")
        plt.close()

        # Clean Spectrogram
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(clean, sr=SAMPLE_RATE, hop_length=HOP_LENGTH,
                                 x_axis='time', y_axis='linear', cmap='viridis')
        plt.title("Clean Spectrogram (Sample 0)")
        plt.colorbar(label="Normalized dB")
        plt.tight_layout()
        plt.savefig("clean_sample_0.png")
        plt.close()

        print("Saved degraded_sample_0.png and clean_sample_0.png")
