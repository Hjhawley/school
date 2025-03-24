#!/bin/bash

model_name=a

time ./cnn_classification.py cnn-fit \
     --model-name ${model_name} --model-file ${model_name}.joblib \
     --batch-number 1

time ./cnn_classification.py learning-curve \
     --model-file ${model_name}.joblib
mv ${model_name}.joblib.learning_curve.png ${model_name}.joblib.learning_curve-a.png

time ./cnn_classification.py cnn-refit \
     --model-name ${model_name} --model-file ${model_name}.joblib \
     --batch-number 2

time ./cnn_classification.py learning-curve \
     --model-file ${model_name}.joblib
mv ${model_name}.joblib.learning_curve.png ${model_name}.joblib.learning_curve-b.png

time ./cnn_classification.py cnn-refit \
     --model-name ${model_name} --model-file ${model_name}.joblib \
     --batch-number 3

time ./cnn_classification.py learning-curve \
     --model-file ${model_name}.joblib
mv ${model_name}.joblib.learning_curve.png ${model_name}.joblib.learning_curve-c.png

time ./cnn_classification.py score \
     --model-file ${model_name}.joblib \
     --batch-number 6
