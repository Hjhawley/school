#!/usr/bin/env python3

import sklearn
import sklearn.preprocessing
import sklearn.linear_model
import joblib

# read data, define fields, etc.
from showcase_common_fine import *

# peek at data
print(data.head(5))

# scale data with x' = (x - u) / s
scaler = sklearn.preprocessing.StandardScaler()
# find u and s
scaler.fit(X_train) 
# transform data
X_train = scaler.transform(X_train) 

# peek at scaled data
print("Scaled Features")
print(feature_names)
print(X_train[:5,:])

# do the fit/training
regressor = sklearn.linear_model.SGDRegressor(max_iter=10000)
regressor.fit(X_train, y_train)

# save the trained model
joblib.dump((regressor,scaler), model_filename)
