import os
import numpy as np
import librosa
import soundfile as sf
import tensorflow as tf
import subprocess
from scipy.signal.windows import hann

# config
SAMPLE_RATE = 44100
WINDOW_DURATION = 5.0     # seconds
WINDOW_STRIDE = 2.5       # seconds
N_FFT = 1024
HOP_LENGTH = 256
WIN_LENGTH = 1024
MODEL_PATH = "models/audio_decompressor_latest.keras"


def preprocess_audio(y):
    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH, win_length=WIN_LENGTH))
    log_S = librosa.amplitude_to_db(S, ref=np.max)
    norm_S = (log_S + 80) / 80
    return norm_S.astype(np.float32)[..., np.newaxis]


def postprocess_spectrogram(mag_spec):
    db = mag_spec * 80 - 80
    mag = librosa.db_to_amplitude(db)
    return librosa.griffinlim(mag, n_fft=N_FFT, hop_length=HOP_LENGTH, win_length=WIN_LENGTH)


def restore_audio(input_path, output_path):
    model = tf.keras.models.load_model(MODEL_PATH)
    y, _ = librosa.load(input_path, sr=SAMPLE_RATE, mono=True)
    total_samples = len(y)
    window_size = int(WINDOW_DURATION * SAMPLE_RATE)
    stride_size = int(WINDOW_STRIDE * SAMPLE_RATE)

    output = np.zeros(total_samples)
    weight = np.zeros(total_samples)
    hann_window = hann(window_size, sym=False)

    for start in range(0, total_samples - window_size + 1, stride_size):
        chunk = y[start:start + window_size]
        input_spec = preprocess_audio(chunk)
        input_spec = np.expand_dims(input_spec, axis=0)

        output_spec = model.predict(input_spec)[0]
        y_hat = postprocess_spectrogram(output_spec.squeeze())

        y_hat = y_hat[:window_size]
        output[start:start + window_size] += y_hat * hann_window
        weight[start:start + window_size] += hann_window

    weight[weight == 0] = 1e-8
    output /= weight

    temp_wav = "temp_output.wav"
    sf.write(temp_wav, output, SAMPLE_RATE)
    subprocess.run(["ffmpeg", "-y", "-i", temp_wav, "-b:a", "320k", output_path])
    os.remove(temp_wav)


def launch_gui():
    def select_input():
        path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
        if path:
            input_entry.delete(0, tk.END)
            input_entry.insert(0, path)
            output_entry.delete(0, tk.END)
            output_path = os.path.splitext(path)[0] + "_restored.mp3"
            output_entry.insert(0, output_path)

    def process_audio():
        input_path = input_entry.get()
        output_path = output_entry.get()
        if not os.path.exists(input_path):
            messagebox.showerror("Error", "Input file does not exist.")
            return
        try:
            status_label.config(text="Processing...")
            root.update()
            restore_audio(input_path, output_path)
            messagebox.showinfo("Success", f"Restored MP3 saved to:\n{output_path}")
            status_label.config(text="Done")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            status_label.config(text="Failed")

    root = tk.Tk()
    root.title("MP3 Audio Restorer")
    root.geometry("500x200")

    frame = ttk.Frame(root, padding=10)
    frame.pack(expand=True, fill=tk.BOTH)

    ttk.Label(frame, text="Input Audio File:").pack(anchor="w")
    input_entry = ttk.Entry(frame, width=60)
    input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    ttk.Button(frame, text="Browse", command=select_input).pack(side=tk.RIGHT)

    ttk.Label(frame, text="Output MP3 File:").pack(anchor="w", pady=(10, 0))
    output_entry = ttk.Entry(frame, width=60)
    output_entry.pack(fill=tk.X)

    ttk.Button(frame, text="Restore Audio", command=process_audio).pack(pady=10)

    status_label = ttk.Label(frame, text="Idle", foreground="gray")
    status_label.pack()

    root.mainloop()


def launch_cli():
    parser = argparse.ArgumentParser(description="Restore degraded MP3 or WAV using trained audio model.")
    parser.add_argument("input", help="Path to degraded input audio file (MP3 or WAV)")
    parser.add_argument("output", help="Path to save restored MP3 output")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file does not exist: {args.input}")
        return

    try:
        print("Restoring audio...")
        restore_audio(args.input, args.output)
        print(f"Restored MP3 saved to: {args.output}")
    except Exception as e:
        print(f"Failed to restore audio: {e}")


GUI = False
if __name__ == "__main__":
    if GUI:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        from tkinter import ttk
        launch_gui()
    else:
        import argparse
        launch_cli()
