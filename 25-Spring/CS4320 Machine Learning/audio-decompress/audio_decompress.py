#!/usr/bin/env python3

from open_data import get_streaming_dataset
from model_creation import create_model
import tensorflow as tf

# Check for GPU
gpus = tf.config.list_physical_devices('GPU')
print("Num GPUs Available:", len(gpus))
print("Using GPU:", bool(gpus))

class Args:
    model_name = "a"


# Load streaming training data
train_ds = get_streaming_dataset("data/train/cut/degraded", "data/train/cut/clean", batch_size=8)

# Inspect shape of a single batch to infer input shape
for X_batch, y_batch in train_ds.take(1):
    input_shape = X_batch.shape[1:]  # Drop batch dim, keep (513, 862, 1)
    break

# Create model
model = create_model(Args(), input_shape=input_shape)

# Train model
model.fit(train_ds, epochs=3)  # No validation yet, just basic training loop

# Save model
model.save("models/audio_decompressor.keras")
print("Model saved to models/audio_decompressor.keras")
