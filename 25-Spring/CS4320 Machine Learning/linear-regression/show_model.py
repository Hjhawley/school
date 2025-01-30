#!/usr/bin/env python3

import joblib

# read data, define fields, etc.
from data_common import *

regressor, scaler = joblib.load(model_filename)

def show_model(regressor):
    print("Model Information:")
    print("coef_: {}".format(regressor.coef_))
    print("intercept_: {}".format(regressor.intercept_))
    print("n_iter_: {}".format(regressor.n_iter_))
    print("n_features_in_: {}".format(regressor.n_features_in_))
    return

def show_function(regressor):
    """
    Reconstruct view of function from coefficients
    """
    offset = regressor.intercept_[0]
    s = "{:6.3f}".format(offset)

    # term for each feature
    for i in range(0, len(regressor.coef_)):
        if len(feature_names[i]) > 0:
            t = "({:6.3f}*{})".format(regressor.coef_[i], feature_names[i])
        if len(s) > 0:
            s += " + "
        s += t

    print("Function:")
    print("{}".format(s))
    return

show_model(regressor)
print()
show_function(regressor)
