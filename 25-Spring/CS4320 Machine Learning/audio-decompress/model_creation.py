import keras


def create_model(args, input_shape):
    """
    Control function to select a model variant by name ("a", "b", "c")
    Returns a compiled model
    """
    create_functions = {
        "a": create_unet_baseline,
    }

    if args.model_name not in create_functions:
        raise ValueError(f"Invalid model name: {args.model_name} not in {list(create_functions.keys())}")

    model = create_functions[args.model_name](args, input_shape)
    print(model.summary())
    return model


def create_unet_baseline(args, input_shape):
    """
    Basic encoder-decoder CNN for audio spectrogram denoising
    Input/Output shapes: (freq, time, 1)
    """
    inputs = keras.layers.Input(shape=input_shape)

    # Encoder
    x = keras.layers.Conv2D(64, (3, 3), padding="same", activation="relu")(inputs)
    x = keras.layers.AveragePooling2D((2, 2), padding="same")(x)
    x = keras.layers.Conv2D(128, (3, 3), padding="same", activation="relu")(x)
    x = keras.layers.AveragePooling2D((2, 2), padding="same")(x)

    # Bottleneck
    x = keras.layers.Conv2D(256, (3, 3), padding="same", activation="relu")(x)

    # Decoder
    x = keras.layers.UpSampling2D((2, 2), interpolation="nearest")(x)
    x = keras.layers.Conv2D(128, (3, 3), padding="same", activation="relu")(x)
    x = keras.layers.UpSampling2D((2, 2), interpolation="nearest")(x)
    x = keras.layers.Cropping2D(((1, 2), (1, 1)))(x)  # Crop to (513, 862) to match
    x = keras.layers.Conv2D(64, (3, 3), padding="same", activation="relu")(x)

    # Output layer
    outputs = keras.layers.Conv2D(1, (1, 1), activation="sigmoid", padding="same")(x)

    model = keras.models.Model(inputs, outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="mse",
        metrics=["mae"]
    )
    return model


# Test
if __name__ == "__main__":
    class Args: model_name = "a"
    dummy_input_shape = (513, 862, 1)  # match the spectrogram shape
    model = create_model(Args(), dummy_input_shape)
