#!/usr/bin/env python3

import sklearn
import sklearn.preprocessing
import sklearn.linear_model
import joblib

# read data, define fields, etc.
from data_common import *

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

# train (try different models)
regressor = sklearn.linear_model.ElasticNet(alpha=1.0, l1_ratio=0.5)
regressor.fit(X_train, y_train)

# save the trained model
joblib.dump((regressor,scaler), model_filename)
