#!/usr/bin/env python3

"""
Download and store titanic data set as CSV.
"""
import pandas as pd
import sklearn.datasets

data = sklearn.datasets.fetch_openml(name='titanic', version=1, parser='auto')
X, y = data['data'], data['target']
df = X.join(y)
df.to_csv("titanic.csv", index=True)
