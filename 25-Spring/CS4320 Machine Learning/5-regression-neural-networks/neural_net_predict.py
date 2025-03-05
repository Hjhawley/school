#!/usr/bin/env python3

import pandas as pd
import tensorflow as tf
import keras

label = "label"
input_filename = "test-preprocessed.csv"
model_filename = "model.keras"
predictions_filename = "predictions.csv"

# Load test data
dataframe = pd.read_csv(input_filename, index_col=0)
if label in dataframe.columns:
    X = dataframe.drop(label, axis=1)
else:
    X = dataframe

# Convert to tf dataset
y_hat = keras.models.load_model(model_filename).predict(X)

# Construct a dataframe with predictions
results_df = pd.DataFrame({
    "Index": dataframe.index,
    label: y_hat[:, 0]  # flatten if needed
})
results_df.to_csv(predictions_filename, index=False)
print("Predictions saved to", predictions_filename)
