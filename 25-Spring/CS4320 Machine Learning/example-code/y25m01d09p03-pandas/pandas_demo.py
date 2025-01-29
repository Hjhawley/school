#!/usr/bin/env python3

import sys
import pandas as pd

def main(argv):
    # read csv file into a DataFrame
    filename = "titanic.csv"
    data = pd.read_csv(filename, dtype={"Cabin": str})

    # first few rows of the DataFrame
    print(data.head())

    # one column (Series) of the DataFrame
    print()
    print("Age")
    print(data["Age"])
    # print(data[["Age", "Survived"]])
    
    # one column (Series) of the DataFrame
    print()
    print("Children")
    print(data[data["Age"] < 10])
    
    print()
    print("Women")
    print(data[data["Sex"] == "female"])
    
    print()
    print("Women and Children")
    print(data[(data["Sex"] == "female") | (data["Age"] < 10)][["Survived", "Name", "Age", "Sex"]])
    
    print()
    print("FemaleChildren")
    print(data[(data["Sex"] == "female") & (data["Age"] < 10)][["Survived", "Name", "Age", "Sex"]])


    print()
    print(data["Age"].sum())
    print(data["Age"].mean())
    
    return

if __name__ == "__main__":
    main(sys.argv)
