# cnn.py
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import RandomFlip, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from preprocess import IMG_SIZE, get_data

# Load data and type mapping from preprocess.py
X_train, X_val, y_train, y_val, type_to_index = get_data()
num_types = len(type_to_index)

# Build the CNN model with on-the-fly horizontal flip augmentation
model = Sequential([
    # RandomFlip applies a horizontal flip to all images during training
    RandomFlip("horizontal", input_shape=(IMG_SIZE[0], IMG_SIZE[1], 1)),
    Conv2D(32, (3, 3), activation='relu'),
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

# Train the model
history = model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))
