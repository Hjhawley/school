#!/usr/bin/env python3

import joblib

# read data, define fields, etc.
from data_common import *

(regressor,scaler) = joblib.load(model_filename)

def show_model(scaler, regressor):
    print("Scaler Information:")
    print("scale_: {}".format(scaler.scale_))
    print("mean_: {}".format(scaler.mean_))
    print("var_: {}".format(scaler.var_))
    print("feature_names_in_: {}".format(scaler.feature_names_in_))
    print("")
    print("Model Information:")
    print("coef_: {}".format(regressor.coef_))
    print("intercept_: {}".format(regressor.intercept_))
    print("n_iter_: {}".format(regressor.n_iter_))
    print("n_features_in_: {}".format(regressor.n_features_in_))
    return

def show_function(scaler, regressor):
    """
    Reconstruct view of function from coefficients
    """
    # Reverse the scaler constants for unraveling the original function
    scale = 1.0 / scaler.scale_
    offset = scaler.mean_ / scaler.scale_
    
    # full offset
    intercept_offset = 0.0
    for i in range(len(regressor.coef_)):
        intercept_offset += regressor.coef_[i] * offset[i]
    s = "{:6.3f}".format(regressor.intercept_[0]-intercept_offset)

    # term for each feature
    for i in range(0, len(regressor.coef_)):
        if len(feature_names[i]) > 0:
            t = "({:6.3f}*{})".format(regressor.coef_[i]*scale[i], feature_names[i])
        if len(s) > 0:
            s += " + "
        s += t

    print()
    print("Function with scaler corrections")
    print(s)
    return

show_model(scaler, regressor)
print()
show_function(scaler, regressor)
