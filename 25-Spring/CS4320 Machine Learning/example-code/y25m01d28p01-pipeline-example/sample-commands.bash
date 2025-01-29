#!/bin/bash

name=synthetic-data
if [ ! -e "${name}-train.csv" ]; then
    echo splitting data
    ./split_data.py split --data-file ${name}.csv
fi
if [ ! -e "${name}-scatter-x1-x2-x3.pdf" ]; then
    echo displaying data
    ./display_data.py all --data-file ${name}.csv
fi
if [ ! -e "${name}-model.joblib" ]; then
    ./pipeline.py SGD --train-file ${name}-train.csv --use-polynomial-features 0 --use-scaler 0 --numerical-missing-strategy mean
fi
if [ -e "${name}-model.joblib" ]; then
    ./pipeline.py show-function --train-file ${name}-train.csv
    ./pipeline.py score --train-file ${name}-train.csv
    ./pipeline.py loss --train-file ${name}-train.csv
fi


# ./pipeline.py SGD --train-file ${name}-train.csv --use-polynomial-features 2 --use-scaler 1
# ./pipeline.py show-model --train-file ${name}-train.csv
#./pipeline.py loss --train-file ${name}-train.csv --show-test 1
#./pipeline.py score --train-file ${name}-train.csv --show-test 1

