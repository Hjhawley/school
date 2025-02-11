#!/usr/bin/env python3

import sklearn.pipeline
import sklearn.base
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import pandas as pd

class DataFrameSelector(sklearn.base.BaseEstimator, sklearn.base.TransformerMixin):
    
    def __init__(self, do_predictors=True, do_numerical=True):
        self.mCategoricalPredictors = ["RoofMatl"]
        self.mNumericalPredictors = ["OverallQual", "GrLivArea", "1stFlrSF", "GarageCars", "YearRemodAdd"]
        self.mLabels = ["SalePrice"]
        self.do_numerical = do_numerical
        self.do_predictors = do_predictors
        
        if do_predictors:
            if do_numerical:
                self.mAttributes = self.mNumericalPredictors
            else:
                self.mAttributes = self.mCategoricalPredictors                
        else:
            self.mAttributes = self.mLabels
            
        return

    def fit( self, X, y=None ):
        # no fit necessary
        self.is_fitted_ = True
        return self

    def transform( self, X, y=None ):
        # only keep columns selected
        values = X[self.mAttributes]
        return values


filename = "train.csv"
data = pd.read_csv(filename, index_col=0)

def make_numeric_pipeline(use_scaler=False, missing_strategy=""):
    items = [("numerical-features-only", DataFrameSelector(do_predictors=True, do_numerical=True))]
    if missing_strategy in ("mean","median","most_frequent"):
        items.append(("imputer", SimpleImputer(strategy=missing_strategy)))
    if use_scaler:
        items.append(("scaler", StandardScaler()))
    return sklearn.pipeline.Pipeline(items)

num_pipeline = make_numeric_pipeline(
    use_scaler=True,
    missing_strategy="median"
)

def make_categorical_pipeline():
    items = ("categorical-features-only", DataFrameSelector(do_predictors=True, do_numerical=False))
    items.append(("onehot", OneHotEncoder(handle_unknown='ignore')))
    return sklearn.pipeline.Pipeline(items)

cat_pipeline = make_categorical_pipeline()
cat_pipeline.fit(data)
data_transform = cat_pipeline.transform(data)
print(data_transform)



items = []

items.append(("numerical", num_pipeline))
items.append(("categorical", cat_pipeline))
pipeline = sklearn.pipeline.FeatureUnion(transformer_list=items)

pipeline.fit(data)
data_transform = pipeline.transform(data)
print(data_transform)
