#!/usr/bin/env python3

import pandas as pd
import sklearn

filename = "showcase-prepared.csv"
train_filename = "showcase-prepared-train.csv"
test_filename = "showcase-prepared-test.csv"
data = pd.read_csv(filename)
seed = 42
ratio = 0.2
data_train, data_test = \
    sklearn.model_selection.train_test_split(data, test_size=ratio, random_state=seed)

data_train.to_csv(train_filename)
data_test.to_csv(test_filename)
