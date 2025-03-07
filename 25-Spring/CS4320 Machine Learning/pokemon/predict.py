# predict.py
import os
import sys
import csv
import numpy as np
import tensorflow as tf
import json
from preprocess import IMG_SIZE, preprocess_image, get_data

def load_type_mapping(json_path="pokemon_types_processed.json"):
    """
    Loads the processed JSON and builds type-to-index and index-to-type mappings.
    """
    with open(json_path, "r") as f:
        type_mapping = json.load(f)
    unique_types = set()
    for types in type_mapping.values():
        unique_types.update(types)
    type_to_index = {t: i for i, t in enumerate(sorted(unique_types))}
    index_to_type = {i: t for t, i in type_to_index.items()}
    return type_to_index, index_to_type

def predict_image(image_path, model, index_to_type):
    """
    Loads and preprocesses the image, then uses the model to predict type probabilities.
    Returns the two type names with the highest probabilities and the full probability array.
    """
    img = preprocess_image(image_path)
    img = np.expand_dims(img, axis=0)  # add batch dimension
    preds = model.predict(img)[0]
    # Get the indices of the top two predictions
    sorted_indices = preds.argsort()[::-1]
    top_two_indices = sorted_indices[:2]
    predicted_labels = [index_to_type[i] for i in top_two_indices]
    return predicted_labels, preds

if __name__ == "__main__":
    # Load the trained model
    model = tf.keras.models.load_model("model.keras")
    type_to_index, index_to_type = load_type_mapping()

    # Get validation file paths from preprocess.py
    _, _, _, _, _, paths_val, _ = get_data()

    # Prepare CSV file to record predictions
    csv_filename = "validation_predictions.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["image_path", "top_two_predictions", "full_probabilities"])
        for img_path in paths_val:
            predicted_labels, probabilities = predict_image(img_path, model, index_to_type)
            writer.writerow([img_path, ",".join(predicted_labels), probabilities.tolist()])
    print("Predictions saved to", csv_filename)
