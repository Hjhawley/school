#!/usr/bin/env python3

import sklearn
import joblib

# read data, define fields, etc.
from data_common import *
test_filename = "data-test.csv"
test_data = pd.read_csv(test_filename, index_col=0)
X_test = test_data[feature_names]
y_test = test_data[label_name]

# load model
(regressor,scaler) = joblib.load(model_filename)

# scale data with already fit scaler
X_test = scaler.transform(X_test)

# ask model to score the data
score_test = regressor.score(X_test, y_test)
print("R^2: {}".format(score_test))

# show mean square error and mean absolute error
y_predicted = regressor.predict(X_test)
loss_test = sklearn.metrics.mean_squared_error(y_test, y_predicted)
print("MSE: {}".format(loss_test))
loss_test = sklearn.metrics.mean_absolute_error(y_test, y_predicted)
print("MAE: {}".format(loss_test))
