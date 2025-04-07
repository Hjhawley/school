#!/usr/bin/env python3

def load_audio_pair(wav_path_1, wav_path_2):
    # Load both WAVs, convert to log-mel spectrograms, return as tensors
    return degraded_spec_tensor, clean_spec_tensor

def load_dataset(degraded_dir, clean_dir):
    # Match filenames, load and pair all files
    # Optionally normalize
    return X, y  # as torch tensors or NumPy arrays

def get_dataloaders(train_paths, val_split=0.15, batch_size=16):
    # Return torch.utils.data.DataLoader objects for training & validation
    return train_loader, val_loader
