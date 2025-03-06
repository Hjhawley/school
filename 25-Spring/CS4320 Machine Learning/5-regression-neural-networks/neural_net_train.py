#!/usr/bin/env python3

import pandas as pd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# Load the preprocessed training data
input_filename = "train-preprocessed.csv"
train_ratio = 0.80

dataframe = pd.read_csv(input_filename, index_col=0)
label = dataframe.columns[-1]  # last column is our regression target
X = dataframe.drop(label, axis=1)
y = dataframe[label]


# Create a TensorFlow dataset and find shape
dataset = tf.data.Dataset.from_tensor_slices((X, y))

for features, labels in dataset.take(1):
    input_shape = features.shape

# Determine train/val split
dataset_size = dataset.cardinality().numpy()
train_size = int(train_ratio * dataset_size)
validate_size = dataset_size - train_size
train_dataset = dataset.take(train_size)
validation_dataset = dataset.skip(train_size)

# Shuffle & Batch
train_dataset = train_dataset.shuffle(buffer_size=train_size)
validation_dataset = validation_dataset.shuffle(buffer_size=validate_size)
BATCH_SIZE = 32
train_dataset = train_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
validation_dataset = validation_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)


# Build the regression model
model = keras.Sequential([
    keras.layers.Input(shape=input_shape),
    keras.layers.Dense(64, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.Dropout(0.4),
    keras.layers.Dense(32, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(1)
])


# Choose loss, optimizer, metrics
model.compile(
    loss="msle",  
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    metrics=["mae"]
)


# Learning rate scheduling & early stopping
def lr_scheduler(epoch, lr):
    # After 10 epochs, decay the LR exponentially
    if epoch >= 10:
        return lr * tf.math.exp(-0.01)
    return lr

learning_rate_callback = keras.callbacks.LearningRateScheduler(lr_scheduler)
early_stop_callback = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)


# Train the model
epoch_count = 50
history = model.fit(
    train_dataset,
    epochs=epoch_count,
    validation_data=validation_dataset,
    callbacks=[learning_rate_callback, early_stop_callback]
)


# Plot learning curves and save the model
epochs = len(history.epoch)
pd.DataFrame(history.history).plot(
    figsize=(8, 5),
    xlim=[0, epochs - 1],
    grid=True,
    xlabel="Epoch"
)
plt.title("Learning Curves")
plt.savefig("learning-curve.png")
plt.clf()

model.save("model.keras")
