#!/usr/bin/env python3

import pandas as pd
import tensorflow as tf
import keras

# Kaggle expects the "id" column and "Premium Amount"
id_column = "id"  # Adjust if your dataset uses a different column name
prediction_column = "Premium Amount"

input_filename = "test-preprocessed.csv"
model_filenames = ["model-2.keras", "model-best.keras"]
predictions_filenames = ["predictions-2.csv", "predictions-best.csv"]

# Load test data
dataframe = pd.read_csv(input_filename, index_col=0)  # Ensure the index column is correctly handled

# Extract features (without labels, if present)
if prediction_column in dataframe.columns:
    X = dataframe.drop(prediction_column, axis=1)
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
        id_column: dataframe.index,
        prediction_column: y_hat[:, 0]  # Flatten if needed
    })
    
    # Save predictions
    results_df.to_csv(predictions_filename, index=False)
    print(f"Predictions saved to {predictions_filename}")
