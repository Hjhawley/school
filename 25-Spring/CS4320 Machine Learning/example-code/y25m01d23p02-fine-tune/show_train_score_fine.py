#!/usr/bin/env python3

import sklearn
import joblib

# read data, define fields, etc.
from showcase_common_fine import *

# load model
(regressor,scaler) = joblib.load(model_filename)

# scale data with already fit scaler
X_train = scaler.transform(X_train)

# ask model to score the data
score_train = regressor.score(X_train, y_train)
print("R^2: {}".format(score_train))

# show mean square error and mean absolute error
y_predicted = regressor.predict(X_train)
loss_train = sklearn.metrics.mean_squared_error(y_train, y_predicted)
print("MSE: {}".format(loss_train))
loss_train = sklearn.metrics.mean_absolute_error(y_train, y_predicted)
print("MAE: {}".format(loss_train))

