import os
import json
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Define image size and directory locations
IMG_SIZE = (96, 96)
IMAGE_DIR = 'pokemon_sprites'
JSON_PATH = 'pokemon_types.json'

# Step 1: Load JSON mapping and build list of file paths and raw labels
def load_data(image_dir, json_path):
    with open(json_path) as f:
        type_mapping = json.load(f)
    image_paths = []
    labels = []
    for dex, types in type_mapping.items():
        file_path = os.path.join(image_dir, f"{dex}.png")
        if os.path.exists(file_path):
            image_paths.append(file_path)
            labels.append(types)
    return image_paths, labels

# Step 2: Create a mapping from type names to indices
def build_type_index(labels):
    unique_types = set()
    for type_list in labels:
        for t in type_list:
            unique_types.add(t)
    type_to_index = {t: i for i, t in enumerate(sorted(unique_types))}
    return type_to_index

# Step 3: Multi-hot encode a list of types
def multi_hot_encode(label_list, type_to_index):
    num_types = len(type_to_index)
    multi_hot = np.zeros(num_types, dtype=np.float32)
    for t in label_list:
        multi_hot[type_to_index[t]] = 1.0
    return multi_hot

# Step 4: Preprocess a single image
def preprocess_image(image_path):
    # Read in grayscale mode, resize and normalize
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, IMG_SIZE)
    img = img.astype('float32') / 255.0
    # Expand dimensions so shape becomes (height, width, 1)
    img = np.expand_dims(img, axis=-1)
    return img

# Step 5: Create dataset arrays from image paths and labels
def create_dataset(image_paths, labels, type_to_index):
    X, y = [], []
    for path, label in zip(image_paths, labels):
        img = preprocess_image(path)
        X.append(img)
        y.append(multi_hot_encode(label, type_to_index))
    return np.array(X), np.array(y)

# Load data and build type mapping
image_paths, raw_labels = load_data(IMAGE_DIR, JSON_PATH)
type_to_index = build_type_index(raw_labels)

# Create dataset arrays
X, y = create_dataset(image_paths, raw_labels, type_to_index)

# Split dataset into training and validation sets (80/20 split)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
print("Training data shape:", X_train.shape, y_train.shape)
print("Validation data shape:", X_val.shape, y_val.shape)

# Step 6: Build a simple CNN model using Keras
num_types = len(type_to_index)
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(num_types, activation='sigmoid')  # Sigmoid for multi-label output
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# Step 7: Train the model
history = model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))
