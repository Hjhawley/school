#!/usr/bin/env python3

from open_data import get_streaming_dataset
from model_creation import create_model
import os
os.environ["TF_GPU_ALLOCATOR"] = "cuda_malloc_async"
import tensorflow as tf

# Check for GPU
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
print("Num GPUs Available:", len(gpus))
print("Using GPU:", bool(gpus))

class Args:
    model_name = "a"

# Load streaming training data (limit to 1000 batches)
train_ds = get_streaming_dataset("data/train/cut/degraded", "data/train/cut/clean", batch_size=1)
train_ds = train_ds.take(1000)

# Inspect shape of a single batch to infer input shape
for X_batch, y_batch in train_ds.take(1):
    input_shape = X_batch.shape[1:]  # Drop batch dim, keep (513, 862, 1)
    break

# Create model
model = create_model(Args(), input_shape=input_shape)

# Train and save model after each epoch
for epoch in range(3):
    print(f"\nStarting epoch {epoch + 1}")
    model.fit(train_ds, epochs=1)
    model.save(f"models/audio_decompressor_epoch{epoch + 1}.keras")
    print(f"Saved model: models/audio_decompressor_epoch{epoch + 1}.keras")
