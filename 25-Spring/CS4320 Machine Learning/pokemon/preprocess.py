# preprocess.py
import os
import json
import numpy as np
import cv2
from sklearn.model_selection import train_test_split

# Define image size and directory locations
IMG_SIZE = (96, 96)
IMAGE_DIR = 'pokemon_sprites'
JSON_PATH = 'pokemon_types.json'
PROCESSED_JSON_PATH = 'pokemon_types_processed.json'

def preprocess_json_file(input_json_path, output_json_path, placeholder="none"):
    """
    Loads the JSON file, and for any Pokémon with only one type,
    appends a placeholder so that every Pokémon has two types.
    """
    with open(input_json_path, "r") as f:
        type_mapping = json.load(f)
    # Process each entry: if only one type, append the placeholder
    for dex, types in type_mapping.items():
        if len(types) == 1:
            type_mapping[dex] = types + [placeholder]
    # Save the processed JSON mapping
    with open(output_json_path, "w") as f:
        json.dump(type_mapping, f, indent=4)
    return type_mapping

def load_data(image_dir, processed_json_path):
    """
    Loads the JSON mapping from the processed JSON file and builds lists
    of image file paths and raw labels.
    """
    with open(processed_json_path) as f:
        type_mapping = json.load(f)
    image_paths = []
    labels = []
    for dex, types in type_mapping.items():
        file_path = os.path.join(image_dir, f"{dex}.png")
        if os.path.exists(file_path):
            image_paths.append(file_path)
            labels.append(types)
    return image_paths, labels

def build_type_index(labels):
    """
    Creates a mapping from type names to indices.
    """
    unique_types = set()
    for type_list in labels:
        for t in type_list:
            unique_types.add(t)
    type_to_index = {t: i for i, t in enumerate(sorted(unique_types))}
    return type_to_index

def multi_hot_encode(label_list, type_to_index):
    """
    Converts a list of types into a multi-hot encoded vector.
    """
    num_types = len(type_to_index)
    multi_hot = np.zeros(num_types, dtype=np.float32)
    for t in label_list:
        multi_hot[type_to_index[t]] = 1.0
    return multi_hot

def preprocess_image(image_path, img_size=IMG_SIZE):
    """
    Loads an image in color, converts it from BGR (OpenCV default) to RGB, 
    resizes it to IMG_SIZE, normalizes the pixels, and returns an image tensor.
    """
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, img_size)
    img = img.astype('float32') / 255.0
    return img

def create_dataset(image_paths, labels, type_to_index):
    """
    Creates NumPy arrays for images (X) and their multi-hot encoded labels (y).
    """
    X, y = [], []
    for path, label in zip(image_paths, labels):
        img = preprocess_image(path)
        X.append(img)
        y.append(multi_hot_encode(label, type_to_index))
    return np.array(X), np.array(y)

def get_data():
    """
    Preprocesses the JSON (if needed), loads data, and splits it into training and validation sets.
    Returns:
      X_train, X_val, y_train, y_val, paths_train, paths_val, type_to_index
    """
    # Preprocess JSON only if the processed file doesn't exist
    if not os.path.exists(PROCESSED_JSON_PATH):
        preprocess_json_file(JSON_PATH, PROCESSED_JSON_PATH)
    
    image_paths, raw_labels = load_data(IMAGE_DIR, PROCESSED_JSON_PATH)
    type_to_index = build_type_index(raw_labels)
    X, y = create_dataset(image_paths, raw_labels, type_to_index)
    # Also split the image_paths so we know which images belong to which set
    X_train, X_val, y_train, y_val, paths_train, paths_val = train_test_split(
        X, y, image_paths, test_size=0.2, random_state=1996) # update seed here
    return X_train, X_val, y_train, y_val, paths_train, paths_val, type_to_index

# For testing the preprocessing steps independently.
if __name__ == "__main__":
    X_train, X_val, y_train, y_val, paths_train, paths_val, type_to_index = get_data()
    print("Training data shape:", X_train.shape, y_train.shape)
    print("Validation data shape:", X_val.shape, y_val.shape)
    print("Validation image paths:", paths_val[:5])  # Print a few sample paths
    print("Type mapping:", type_to_index)
