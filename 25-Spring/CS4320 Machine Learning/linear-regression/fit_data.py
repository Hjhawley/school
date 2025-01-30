#!/usr/bin/env python3

import sklearn
import sklearn.preprocessing
import sklearn.linear_model
import joblib

# read data, define fields, etc.
from data_common import *

# peek at data
print(data.head(5))

# scale data first
scaler = sklearn.preprocessing.StandardScaler()
scaler.fit(X_train)

# transform dataset
X_train_scaled = scaler.transform(X_train)

# train
regressor = sklearn.linear_model.SGDRegressor(verbose=1, max_iter=10000, random_state=42)
regressor.fit(X_train_scaled, y_train)

# save model and scaler together
joblib.dump((regressor, scaler), model_filename)
print("Model and scaler saved to:", model_filename)
