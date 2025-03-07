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

def at_least_one_accuracy(y_true, y_pred):
    # Computes the fraction of samples for which at least one of the true labels
    # appears in the top-2 predicted labels.

    # Get the top 2 predicted indices for each sample.
    top2 = tf.math.top_k(y_pred, k=2).indices  # shape: (batch_size, 2)
    
    # Convert ground truth to boolean.
    true_mask = tf.cast(y_true, tf.bool)  # shape: (batch_size, num_types)
    
    # For each sample, gather the boolean values at the top2 indices.
    # We use batch_dims=1 so that for each row, we gather from that row.
    top2_true = tf.gather(true_mask, top2, batch_dims=1)  # shape: (batch_size, 2)
    
    # A sample is correct if any of the top2 predictions is True.
    sample_correct = tf.reduce_any(top2_true, axis=1)  # shape: (batch_size,)
    
    # Convert booleans to floats (True -> 1.0, False -> 0.0) and average.
    return tf.reduce_mean(tf.cast(sample_correct, tf.float32))

# Compile the model with your custom metric included
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', at_least_one_accuracy])
model.summary()

# Create a callback that monitors validation at_least_one_accuracy
checkpoint = tf.keras.callbacks.ModelCheckpoint("model.keras",
                               monitor='val_at_least_one_accuracy',
                               mode='max',
                               save_best_only=True,
                               verbose=1)

# Train the model with the checkpoint callback
history = model.fit(X_train, y_train, epochs=50, validation_data=(X_val, y_val), callbacks=[checkpoint])
print("Training complete. Best model saved as model.keras")
