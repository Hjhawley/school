#!/usr/bin/env python3

import pandas as pd
import tensorflow as tf
import keras
import matplotlib.pyplot as plt

input_filename = "train-preprocessed.csv"
train_ratio = 0.80
#
# Load the training dataframe, separate into X/y
#
dataframe = pd.read_csv(input_filename, index_col=0)
label = dataframe.columns[-1] # assume the last column is the label
X = dataframe.drop(label, axis=1)
y = dataframe[label]

print(dataframe)
print(X)
print(y)

#
# Prepare a tensorflow dataset from the dataframe
#
dataset = tf.data.Dataset.from_tensor_slices((X, y))
# print(dataset)
# print(list(dataset.as_numpy_iterator()))
# print(dataset.element_spec)


#
# Find the shape of the inputs and outputs.
# Necessary for the model to have correctly sized input and output layers
#
#
# This is happening *before* batching, so
# the shape does not yet include the batch size
#
for features, labels in dataset.take(1):
    input_shape = features.shape
    output_shape = labels.shape
# print(input_shape)
# print(output_shape)


#
# Split the dataset into train and validation sets.
#
dataset_size       = dataset.cardinality().numpy()
train_size         = int(train_ratio * dataset_size)
validate_size      = dataset_size - train_size
train_dataset      = dataset.take(train_size)
validation_dataset = dataset.skip(train_size)

#
# Cause the datasets to shuffle, internally
#
train_dataset      = train_dataset.shuffle(buffer_size=train_size)
validation_dataset = validation_dataset.shuffle(buffer_size=validate_size)

#
# Cause the datasets to batch.
# Efficiency benefits.
# Training differences.
#
BATCH_SIZE = 32
train_dataset      = train_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
validation_dataset = validation_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)



#
# Build the model
#
tf.random.set_seed(42)

def build_model_1():
    model_filename = "model-1.keras"
    learning_curve_filename = "learning-curve-1.png"
    model = keras.Sequential([
        keras.layers.Input(shape=input_shape),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dense(32, activation="relu"),
        keras.layers.Dense(16, activation="relu"),
        keras.layers.Dense(8, activation="relu"),
        keras.layers.Dense(1, activation="sigmoid")
    ])
    #print(model.summary())
    #print(model.layers[1].get_weights())
    return model, model_filename, learning_curve_filename
    
model, model_filename, learning_curve_filename = build_model_1()

#
# Compile the model
#
loss = "binary_crossentropy"
model.compile(loss=loss,
              optimizer=keras.optimizers.Adam(learning_rate=0.001),
              metrics=["accuracy"])


#
# Update the learning rate dynamically
#
def scheduler(epoch, learning_rate):
    r = learning_rate
    if epoch >= 10:
        r = learning_rate * float(tf.exp(-0.005))
    return r
learning_rate_callback = keras.callbacks.LearningRateScheduler(scheduler)

#
# Stop training if validation loss does not improve
#
early_stop_callback = keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)

#
# Train for up to epoch_count epochs
#
epoch_count = 5
history = model.fit(x=train_dataset,
                    epochs=epoch_count,
                    validation_data=validation_dataset,
                    callbacks=[learning_rate_callback, early_stop_callback])
epochs = len(history.epoch)
# print(history)


#
# Display the learning curves
#
line_style = ["r--", "r--*", "r--+", "b-", "b-*", "b-+"]
line_style = ["r--*", "r--+", "b-*", "b-+"]
pd.DataFrame(history.history).plot(
    figsize=(8, 5), xlim=[0, epochs-1], ylim=[0, 1], grid=True, xlabel="Epoch",
    style=line_style)
# plt.show()
plt.savefig(learning_curve_filename)
plt.clf()


#
# Save the model
#
model.save(model_filename)
