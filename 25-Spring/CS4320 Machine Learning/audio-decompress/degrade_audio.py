import os
import ffmpeg

BITRATE = "96k" # bitrate, let's use 96kbps as a baseline for "poor quality"
SETS = ["train", "test"]
BASE_DIR = "data"

def degrade_set(split):
    input_dir = os.path.join(BASE_DIR, split, "cut", "clean")
    output_dir = os.path.join(BASE_DIR, split, "cut", "degraded")
    os.makedirs(output_dir, exist_ok=True)

    for fname in sorted(os.listdir(input_dir)):
        if not fname.endswith(".wav"):
            continue

        in_path = os.path.join(input_dir, fname)
        out_path = os.path.join(output_dir, fname)
        mp3_temp = in_path.replace(".wav", "_temp.mp3")

        try:
            # Encode to temporary MP3
            ffmpeg.input(in_path).output(mp3_temp, audio_bitrate=BITRATE, acodec='libmp3lame').overwrite_output().run(quiet=True)

            # Decode back to degraded WAV
            ffmpeg.input(mp3_temp).output(out_path, ar=44100).overwrite_output().run(quiet=True)

            os.remove(mp3_temp)  # Clean up temp MP3
        except ffmpeg.Error as e:
            print(f"Failed to process {fname}: {e}")

    print(f"Degraded {split} set saved to {output_dir}")

if __name__ == "__main__":
    for split in SETS:
        degrade_set(split)
