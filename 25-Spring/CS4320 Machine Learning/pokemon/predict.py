# predict.py
import sys
import os
import cv2
import json
import numpy as np
import tensorflow as tf
from preprocess import IMG_SIZE, preprocess_image

# Path to the processed JSON file with type mappings
PROCESSED_JSON_PATH = 'pokemon_types_processed.json'

def load_type_mapping(json_path=PROCESSED_JSON_PATH):
    """
    Loads the processed JSON and builds type-to-index and index-to-type mappings.
    """
    with open(json_path, "r") as f:
        type_mapping = json.load(f)
    # Gather all unique types from the mapping values
    unique_types = set()
    for types in type_mapping.values():
        unique_types.update(types)
    type_to_index = {t: i for i, t in enumerate(sorted(unique_types))}
    index_to_type = {i: t for t, i in type_to_index.items()}
    return type_to_index, index_to_type

def predict_image(image_path, model, index_to_type, threshold=0.5):
    """
    Loads and preprocesses the image, then uses the model to predict type probabilities.
    Returns a list of predicted type names where the probability exceeds the threshold.
    """
    img = preprocess_image(image_path)  # shape: (IMG_SIZE[0], IMG_SIZE[1], 1)
    img = np.expand_dims(img, axis=0)     # add batch dimension: (1, height, width, 1)
    preds = model.predict(img)[0]         # predictions for each label
    predicted_labels = [index_to_type[i] for i, prob in enumerate(preds) if prob >= threshold]
    return predicted_labels, preds

if __name__ == "__main__":
    # Ensure an image path is provided
    if len(sys.argv) < 2:
        print("Usage: python predict.py path_to_image.png")
        sys.exit(1)
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print("Error: Image file does not exist:", image_path)
        sys.exit(1)

    # Load the trained model and the type mapping
    model = tf.keras.models.load_model("model.keras")
    type_to_index, index_to_type = load_type_mapping()

    # Run prediction on the provided image
    predicted_labels, probabilities = predict_image(image_path, model, index_to_type)
    print("Predicted types:", predicted_labels)
    print("Probabilities:", probabilities)
