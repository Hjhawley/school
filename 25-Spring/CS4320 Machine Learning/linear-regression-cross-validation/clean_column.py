#!/usr/bin/env python3

import pandas as pd

filename = "data-train.csv"
data = pd.read_csv(filename, index_col=0)

feature = "BsmtCond"
label = "SalePrice"

series = data[feature]
print(series.shape)
series = series.dropna()
print(series.shape)

# reduced dataframe

df2 = data[[feature,label]].dropna()
print(df2.shape)



