#!/usr/bin/env python3

import pandas as pd
import tensorflow as tf
import keras

label = "label"
input_filename = "test-preprocessed.csv"
model_filenames = ["model-2.keras", "model-best.keras"]
predictions_filenames = ["predictions-2.csv", "predictions-best.csv"]

# Load test data
dataframe = pd.read_csv(input_filename, index_col=0)

if label in dataframe.columns:
    X = dataframe.drop(label, axis=1)
else:
    X = dataframe

# Iterate over both models and generate predictions
for model_filename, predictions_filename in zip(model_filenames, predictions_filenames):
    # Load model
    model = keras.models.load_model(model_filename)
    
    # Make predictions
    y_hat = model.predict(X)
    
    # Construct a dataframe with predictions
    results_df = pd.DataFrame({
        "Index": dataframe.index,
        label: y_hat[:, 0]  # Flatten if needed
    })
    
    # Save predictions
    results_df.to_csv(predictions_filename, index=False)
    print(f"Predictions saved to {predictions_filename}")
