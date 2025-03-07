# cnn.py
import tensorflow as tf
from preprocess import IMG_SIZE, get_data

# Load training data (we don't need validation paths here)
X_train, X_val, y_train, y_val, _, _, type_to_index = get_data()
num_types = len(type_to_index)

# Build the CNN model with on-the-fly horizontal flip augmentation
model = tf.keras.models.Sequential([
    tf.keras.layers.RandomFlip("horizontal", input_shape=(IMG_SIZE[0], IMG_SIZE[1], 1)),
    
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu', 
                           kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D((2, 2)),
    
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu', 
                           kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D((2, 2)),
    
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu', 
                           kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D((2, 2)),
    
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(num_types, activation='sigmoid')  # Multi-label output
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# Train the model
history = model.fit(X_train, y_train, epochs=50, validation_data=(X_val, y_val))

# Save the model
model.save("model.keras")
print("Model saved as model.keras")
