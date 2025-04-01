import os
import zipfile
import urllib.request
from pydub import AudioSegment
import ffmpeg
import librosa
import numpy as np
import torch
from sklearn.model_selection import train_test_split

SAMPLE_RATE = 44100 # 44.1khz
N_FFT = 1024
HOP_LENGTH = 256
CLIP_LEN_MS = 7000  # 7s

DATA_DIR = "data"
ORIGINAL_CLIPS_DIR = os.path.join(DATA_DIR, "original_wav")
DEGRADED_CLIPS_DIR = os.path.join(DATA_DIR, "degraded_mp3")
RAW_DIR = os.path.join(DATA_DIR, "musdb18")

MUSDB_URL = "https://zenodo.org/record/1117372/files/MUSDB18-7.zip?download=1"
MUSDB_ZIP = os.path.join(DATA_DIR, "musdb18.zip")


def download_and_extract_musdb():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(MUSDB_ZIP):
        print("Downloading MUSDB18...")
        urllib.request.urlretrieve(MUSDB_URL, MUSDB_ZIP)
    if not os.path.exists(RAW_DIR):
        print("Extracting MUSDB18...")
        with zipfile.ZipFile(MUSDB_ZIP, "r") as zip_ref:
            zip_ref.extractall(RAW_DIR)
    print("MUSDB18 ready.")


def split_to_clips(source_dir, out_dir, target_sr=SAMPLE_RATE):
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    for root, _, files in os.walk(source_dir):
        for file in files:
            if not file.endswith(".wav"):
                continue
            path = os.path.join(root, file)
            audio = AudioSegment.from_wav(path).set_frame_rate(target_sr).set_channels(1)
            duration_ms = len(audio)
            for i in range(0, duration_ms - CLIP_LEN_MS, CLIP_LEN_MS):
                clip = audio[i:i+CLIP_LEN_MS]
                clip_path = os.path.join(out_dir, f"clip_{count:05}.wav")
                clip.export(clip_path, format="wav")
                count += 1
    print(f"Saved {count} clips to {out_dir}")


def compress_with_mp3(input_dir, output_dir, bitrate="64k"):
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if not file.endswith(".wav"):
            continue
        in_path = os.path.join(input_dir, file)
        out_path = os.path.join(output_dir, file)
        mp3_temp = in_path.replace(".wav", "_tmp.mp3")
        # Compress to MP3
        ffmpeg.input(in_path).output(mp3_temp, audio_bitrate=bitrate, acodec='libmp3lame').overwrite_output().run(quiet=True)
        # Decode back to WAV
        ffmpeg.input(mp3_temp).output(out_path, ar=SAMPLE_RATE).overwrite_output().run(quiet=True)
        os.remove(mp3_temp)
    print(f"Generated degraded audio in {output_dir}")


if __name__ == "__main__":
    print("STEP 1: Downloading MUSDB18...")
    download_and_extract_musdb()

    print("STEP 2: Splitting WAVs into 7-second clips...")
    wav_root = os.path.join(RAW_DIR, "MUSDB18-7", "test")  # or "train"
    split_to_clips(wav_root, ORIGINAL_CLIPS_DIR)

    print("STEP 3: Creating degraded MP3 clips...")
    compress_with_mp3(ORIGINAL_CLIPS_DIR, DEGRADED_CLIPS_DIR, bitrate="64k")

    print("Data loading and preparation complete.")
