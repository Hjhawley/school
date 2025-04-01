import os
from pydub import AudioSegment
import ffmpeg

# Constants
SAMPLE_RATE = 44100  # 44.1 kHz
CLIP_LEN_MS = 7000   # 7 seconds

# Directory paths
DATA_DIR = "data"
ORIGINAL_CLIPS_DIR = os.path.join(DATA_DIR, "original_wav")
DEGRADED_CLIPS_DIR = os.path.join(DATA_DIR, "degraded_mp3")
RAW_DIR = "path/to/your/musdb18hq"  # Update this to your actual path

def split_to_clips(source_dir, out_dir, target_sr=SAMPLE_RATE):
    """
    Splits audio files in the source directory into 7-second clips and saves them to the output directory.
    """
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".wav"):
                path = os.path.join(root, file)
                audio = AudioSegment.from_wav(path)
                # Ensure audio is in stereo
                if audio.channels == 1:
                    audio = audio.set_channels(2)
                audio = audio.set_frame_rate(target_sr)
                duration_ms = len(audio)
                for i in range(0, duration_ms - CLIP_LEN_MS + 1, CLIP_LEN_MS):
                    clip = audio[i:i + CLIP_LEN_MS]
                    clip_path = os.path.join(out_dir, f"clip_{count:05}.wav")
                    clip.export(clip_path, format="wav")
                    count += 1
    print(f"Saved {count} clips to {out_dir}")

def compress_with_mp3(input_dir, output_dir, bitrate="64k"):
    """
    Compresses WAV files in the input directory to MP3 at the specified bitrate and saves them to the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.endswith(".wav"):
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
    print("STEP 1: Splitting WAVs into 7-second clips...")
    wav_root = os.path.join(RAW_DIR, "train")  # or "test"
    split_to_clips(wav_root, ORIGINAL_CLIPS_DIR)

    print("STEP 2: Creating degraded MP3 clips...")
    compress_with_mp3(ORIGINAL_CLIPS_DIR, DEGRADED_CLIPS_DIR, bitrate="64k")

    print("Data preparation complete.")
