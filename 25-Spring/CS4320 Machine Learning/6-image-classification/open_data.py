#!/usr/bin/env python3

#
# https://keras.io/api/datasets/fashion_mnist/
#
# 60,000 28x28 grayscale training images
# 10,000 28x28 grayscale testing images
#
# I choose to split them into 6 training batches,
# only using 1-5 to train and 6 to validate.
#
#


import numpy as np
import keras

def load_batch_from_keras(number):
    """
    number in [1, 2, 3, 4, 5] -> load training batch
    number == 6 -> load validation batch
    number < 1 -> test batch
    number > 6 -> load training batches 1,2,3,4,5
    """
    (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

    # shuffle training data (always the same seed)
    np.random.seed(42)
    p = np.random.permutation(x_train.shape[0])
    x_train = x_train[p]
    y_train = y_train[p]

    # select subset
    if number < 1:
        images, labels = x_test, y_test
    elif number > 6:
        start = 0 * 10000
        end = 5 * 10000
        images, labels = x_train[start:end], y_train[start:end]
    else:
        start = (number - 1) * 10000
        end = (number) * 10000
        images, labels = x_train[start:end], y_train[start:end]

    # one-hot-encode labels
    labels = keras.utils.to_categorical(labels, num_classes=10)
    # CIFAR-10 is already (32, 32, 3), no reshape needed
    # make sure the data is in float32 and scaled properly
    images = images.astype(np.float32) / 255.0

    return images, labels

def load_batch(number):
    return load_batch_from_keras(number)

