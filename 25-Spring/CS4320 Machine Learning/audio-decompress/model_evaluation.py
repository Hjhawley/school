#!/usr/bin/env python3

# Evaluation script for audio decompression model

import os
import numpy as np
import keras
import tensorflow as tf
from open_data import get_static_batch_dataset


def evaluate_model(model_file, degraded_dir, clean_dir, batch_size=10):
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"Model file '{model_file}' not found")

    print(f"Loading model from {model_file}...")
    model = keras.models.load_model(model_file)

    print("Loading evaluation data...")
    eval_ds = get_static_batch_dataset(degraded_dir, clean_dir, batch_size=batch_size)
    
    print("Evaluating model...")
    loss, mae = model.evaluate(eval_ds)
    print(f"Evaluation Results:\n - Loss: {loss:.4f}\n - MAE: {mae:.4f}")


if __name__ == "__main__":
    MODEL_PATH = "models/audio_decompressor_latest.keras"
    DEGRADED_DIR = "data/val/degraded"
    CLEAN_DIR = "data/val/clean"

    evaluate_model(MODEL_PATH, DEGRADED_DIR, CLEAN_DIR, batch_size=10)
