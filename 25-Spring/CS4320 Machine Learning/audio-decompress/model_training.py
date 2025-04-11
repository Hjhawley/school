#!/usr/bin/env python3

# main script - train the model

import os
os.environ["TF_GPU_ALLOCATOR"] = "cuda_malloc_async"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # suppress unimportant info

from open_data import get_streaming_dataset, get_random_validation_batch
from model_creation import create_model
import tensorflow as tf
import keras
import joblib
from model_history import plot_history


# Enable memory growth
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
print("Num GPUs Available:", len(gpus))
print("Using GPU:", bool(gpus))


class Args:
    model_name = "a"


# Early stopping
early_stop_counter_path = "early_stop_counter.txt"
best_val_loss_path = "best_val_loss.txt"
PATIENCE = 5


# Set how many samples to use per run
samples_per_run = 20

# Load run index (auto-increments each run)
run_index_path = "run_index.txt"
if os.path.exists(run_index_path):
    with open(run_index_path, "r") as f:
        run_index = int(f.read().strip())
else:
    run_index = 0


# Load dataset and apply chunking
train_ds = get_streaming_dataset("data/train/cut/degraded", "data/train/cut/clean", batch_size=1)
train_ds = train_ds.skip(run_index * samples_per_run).take(samples_per_run)


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


# Early stopping
early_stopping_cb = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=PATIENCE,
    restore_best_weights=True
)


# Save checkpoints after each epoch
checkpoint_cb = keras.callbacks.ModelCheckpoint(
    filepath=model_path,
    save_best_only=False,
    save_weights_only=False,
    verbose=1
)


# Set how many epochs to run this session
epochs_this_run = 5


# Train, validate, and save history
X_val, y_val = get_random_validation_batch("data/train/cut/degraded", "data/train/cut/clean", batch_size=4)
val_data = (X_val, y_val)
history = model.fit(
    train_ds,
    validation_data=val_data,
    epochs=loaded_epoch + epochs_this_run,
    initial_epoch=loaded_epoch,
    callbacks=[checkpoint_cb, early_stopping_cb]
)


# Update epoch progress
with open(progress_path, "w") as f:
    f.write(str(loaded_epoch + epochs_this_run))

# Update run index
with open(run_index_path, "w") as f:
    f.write(str(run_index + 1))

# Save training history
joblib.dump(history.history, f"{model_path.replace('.keras', '')}.history")

# Plot learning curve
plot_history(model_path.replace(".keras", ""))

print(f"Model saved, epoch {loaded_epoch + epochs_this_run} complete, chunk #{run_index} done.")

# Evaluate on random validation batch
print("Running validation on a random training subset...")
with tf.device('/CPU:0'):
    val_loss, val_mae = model.evaluate(*val_data, verbose=1)
    print(f"Validation Results:\n - Loss: {val_loss:.4f}\n - MAE: {val_mae:.4f}")

# Early stopping across runs
if os.path.exists(best_val_loss_path):
    with open(best_val_loss_path, "r") as f:
        best_val_loss = float(f.read().strip())
else:
    best_val_loss = float("inf")

if val_loss < best_val_loss:
    print("Validation loss improved. Resetting early stop counter.")
    with open(best_val_loss_path, "w") as f:
        f.write(str(val_loss))
    with open(early_stop_counter_path, "w") as f:
        f.write("0")
else:
    if os.path.exists(early_stop_counter_path):
        with open(early_stop_counter_path, "r") as f:
            counter = int(f.read().strip())
    else:
        counter = 0

    counter += 1
    print(f"No improvement. Early stop counter = {counter}/{PATIENCE}")

    with open(early_stop_counter_path, "w") as f:
        f.write(str(counter))

    if counter >= PATIENCE:
        print("Early stopping triggered. No improvement for 5 chunks.")
        exit(0)
