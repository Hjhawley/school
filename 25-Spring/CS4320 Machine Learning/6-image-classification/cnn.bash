#!/bin/bash

source .venv/bin/activate

model_name=c

time ./cnn_classification.py cnn-fit \
     --model-name ${model_name} --model-file ${model_name}.keras \
     --batch-number 1

time ./cnn_classification.py learning-curve \
     --model-file ${model_name}.keras
mv ${model_name}.keras.learning_curve.png ${model_name}.keras.learning_curve-a.png

time ./cnn_classification.py cnn-refit \
     --model-name ${model_name} --model-file ${model_name}.keras \
     --batch-number 2

time ./cnn_classification.py learning-curve \
     --model-file ${model_name}.keras
mv ${model_name}.keras.learning_curve.png ${model_name}.keras.learning_curve-b.png

time ./cnn_classification.py cnn-refit \
     --model-name ${model_name} --model-file ${model_name}.keras \
     --batch-number 3

time ./cnn_classification.py learning-curve \
     --model-file ${model_name}.keras
mv ${model_name}.keras.learning_curve.png ${model_name}.keras.learning_curve-c.png

time ./cnn_classification.py score \
     --model-file ${model_name}.keras \
     --batch-number 5
