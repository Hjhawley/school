#!/usr/bin/env python3

import sklearn.pipeline
import sklearn.base
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import pandas as pd

class DataFrameSelector(sklearn.base.BaseEstimator, sklearn.base.TransformerMixin):
    
    def __init__(self, do_predictors=True, do_numerical=True):
        self.mCategoricalPredictors = ["MSSubClass", "MSZoning", "Street", "Alley",
                                       "LotShape", "LandContour", "Utilities", 
                                       "LotConfig", "LandSlope", "Neighborhood", 
                                       "Condition1", "Condition2", "BldgType",
                                       "HouseStyle", "RoofStyle", "RoofMatl",
                                       "Exterior1st", "Exterior2nd", "MasVnrType",
                                       "ExterQual", "ExterCond", "Foundation",
                                       "BsmtQual", "BsmtCond", "BsmtExposure",
                                       "BsmtFinType1", "BsmtFinType2", "Heating",
                                       "HeatingQC", "CentralAir", "Electrical", 
                                       "KitchenQual", "Functional", "FireplaceQu", 
                                       "GarageType", "GarageFinish", "GarageQual", 
                                       "GarageCond", "PavedDrive", "PoolQC", 
                                       "Fence", "MiscFeature", "SaleType", 
                                       "SaleCondition"]
        self.mNumericalPredictors = ["LotFrontage", "LotArea", "OverallQual", 
                                     "OverallCond", "YearBuilt", "YearRemodAdd", 
                                     "GrLivArea", "1stFlrSF",
                                     "MasVnrArea", "BsmtFinSF1", "BsmtFinSF2",
                                     "BsmtUnfSF", "TotalBsmtSF", "1stFlrSF", 
                                     "2ndFlrSF", "LowQualFinSF", "GrLivArea", 
                                     "BsmtFullBath", "BsmtHalfBath", "FullBath",
                                     "HalfBath", "BedroomAbvGr", "KitchenAbvGr", 
                                     "TotRmsAbvGrd", "Fireplaces", "GarageYrBlt",
                                     "GarageCars", "GarageArea", "WoodDeckSF", 
                                     "OpenPorchSF", "EnclosedPorch", "3SsnPorch",
                                     "ScreenPorch", "PoolArea", "MiscVal", 
                                     "MoSold", "YrSold"]
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

items = []
items.append(("categorical-features-only", DataFrameSelector(do_predictors=True, do_numerical=False)))
items.append(("onehot", OneHotEncoder(handle_unknown='ignore')))

cat_pipeline = sklearn.pipeline.Pipeline(items)

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
