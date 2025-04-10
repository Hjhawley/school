#!/usr/bin/env python3

import os
os.environ["TF_GPU_ALLOCATOR"] = "cuda_malloc_async"

from open_data import get_streaming_dataset
from model_creation import create_model
import tensorflow as tf
import keras


# Enable memory growth
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
print("Num GPUs Available:", len(gpus))
print("Using GPU:", bool(gpus))

class Args:
    model_name = "a"


# Load training dataset
train_ds = get_streaming_dataset("data/train/cut/degraded", "data/train/cut/clean", batch_size=1)

# Limit dataset per run (uncomment to allow chunking)
# samples_per_run = 500
# run_index = 0  # Update this if i need to
# train_ds = train_ds.skip(run_index * samples_per_run).take(samples_per_run)

# Inspect a batch to infer input shape
for X_batch, y_batch in train_ds.take(1):
    input_shape = X_batch.shape[1:]  # (513, 862, 1)
    break


# Load last saved model if exists
model_path = "models/audio_decompressor_latest.keras"
if os.path.exists(model_path):
    print(f"Loading model from {model_path}")
    model = tf.keras.models.load_model(model_path)
else:
    model = create_model(Args(), input_shape=input_shape)


# Load last epoch if available
progress_path = "training_progress.txt"
if os.path.exists(progress_path):
    with open(progress_path, "r") as f:
        loaded_epoch = int(f.read().strip())
        print(f"Resuming from epoch {loaded_epoch}")
else:
    loaded_epoch = 0


# Save checkpoints after each epoch
checkpoint_cb = keras.callbacks.ModelCheckpoint(
    filepath=model_path,
    save_best_only=False,
    save_weights_only=False,
    verbose=1
)


# Set how many epochs to run this session
epochs_this_run = 1

# Train
model.fit(
    train_ds,
    epochs=loaded_epoch + epochs_this_run,
    initial_epoch=loaded_epoch,
    callbacks=[checkpoint_cb]
)

# Update progress
with open(progress_path, "w") as f:
    f.write(str(loaded_epoch + epochs_this_run))

print(f"Model saved and progress updated to epoch {loaded_epoch + epochs_this_run}")
