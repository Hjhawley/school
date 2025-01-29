#!/usr/bin/env python3

import pandas as pd

###########################################################
# Set global values for filenames, features, label
# Load data
###########################################################

feature_names = ["CP", "Weight", "Height"]

label_name = "Score"
train_filename = "showcase-prepared-train.csv"
data = pd.read_csv(train_filename, index_col=0)
X_train = data[feature_names]
y_train = data[label_name]

model_filename = "showcase-linear-regressor-fine.joblib"
