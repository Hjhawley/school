#!/usr/bin/env python3

import sklearn
import sklearn.linear_model
import joblib

# read data, define fields, etc.
from showcase_common import *

# peek at data
print(data.head(5))

# do the fit/training
regressor = sklearn.linear_model.SGDRegressor(verbose=1)    # this CREATES a model to be trained. verbose = how much feedback you want during training
regressor.fit(X_train, y_train)                             # this TRAINS the model

# save the trained model
joblib.dump(regressor, model_filename)
