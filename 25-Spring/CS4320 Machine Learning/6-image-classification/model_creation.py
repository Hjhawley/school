#!/usr/bin/env python3

#
# Keep the model creation code contained here
#
import tensorflow as tf
import keras

def create_model(my_args, input_shape):
    """
    Control function.
    Selects the correct function to build a model, based on the model name
    from the command line arguments.

    Assumes my_args.model_name is set.
    """
    create_functions = {
        "a": create_model_a,
    }
    if my_args.model_name not in create_functions:
        raise ValueError("Invalid model name: {} not in {}".format(my_args.model_name, list(create_functions.keys())))
        
    model = create_functions[my_args.model_name](my_args, input_shape)
    print(model.summary())
    return model


### Various model architectures

def create_model_a(my_args, input_shape):
    model = keras.models.Sequential()
    model.add(keras.layers.Input(shape=input_shape))
    model.add(keras.layers.Conv2D(filters=64, kernel_size=(7,7), activation="relu", kernel_initializer="he_normal", padding="same"))
    model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))
    model.add(keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation="relu", kernel_initializer="he_normal", padding="same"))
    model.add(keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation="relu", kernel_initializer="he_normal", padding="same"))
    model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(64, activation="relu", kernel_initializer="he_normal"))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(10, activation="softmax"))

    model.compile(loss="categorical_crossentropy", metrics=["accuracy"], optimizer=keras.optimizers.Adam())
    return model
