#!/usr/bin/env python3

import pandas as pd

###########################################################
# Set global values for filenames, features, label
# Load data
###########################################################

#
# CP doesn't appear to be relevant when looking at
# the scatter plots.
# feature_names = ["CP", "Weight", "Height"]
feature_names = ["Weight", "Height"]

label_name = "Score"
train_filename = "showcase-prepared-train.csv"
data = pd.read_csv(train_filename, index_col=0)
X_train = data[feature_names]
y_train = data[label_name]

model_filename = "showcase-linear-regressor.joblib"
