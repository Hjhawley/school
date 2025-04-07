""" #!/usr/bin/env python3

#
# Evaluation of model performance
#

import sklearn.metrics
import numpy as np
import os.path
import joblib
import open_data
import keras


def sklearn_metric(y, yhat):
    """
    Try to pretty-print the confusion matrix as text.
    
    If binary data, then compute precision, recall and F1.
    If multi-class data, then compute classification report.

    Expects y and yhat to be the class number. (*NOT one-hot-encoded*).
    """
    cm = sklearn.metrics.confusion_matrix(y, yhat)
    ###
    header = "+"
    for col in range(cm.shape[1]):
        header += "-----+"
    rows = [header]
    for row in range(cm.shape[0]):
        row_str = "|"
        for col in range(cm.shape[1]):
            row_str += "{:4d} |".format(cm[row][col])
        rows.append(row_str)
    footer = header
    rows.append(footer)
    table = "\n".join(rows)
    print(table)
    print()
    ###
    if cm.shape[0] == 2:
        precision = sklearn.metrics.precision_score(y, yhat)
        recall = sklearn.metrics.recall_score(y, yhat)
        f1 = sklearn.metrics.f1_score(y, yhat)
        print("precision: {}".format(precision))
        print("recall: {}".format(recall))
        print("f1: {}".format(f1))
    else:
        report = sklearn.metrics.classification_report(y, yhat)
        print(report)
    return

def show_score(my_args):
    """
    Textual display of trained model's scores.
    
    Expects y_train to be the class number.
    Expects the model's output to be the proba (probability) for each class.
    """
    model_file = my_args.model_file
    if not os.path.exists(model_file):
        raise Exception("Model file, '{}', does not exist.".format(model_file))

    X_train, y_train = open_data.load_batch(my_args.batch_number)

    model = keras.models.load_model(model_file)
    print(f"X_train.shape: {X_train.shape}, y_train.shape: {y_train.shape}")
    yhat_train_proba = model.predict(X_train)
    yhat_train = np.argmax(yhat_train_proba, axis=1)
    print()
    print("{}: train: ".format(model_file))
    print()
    sklearn_metric(np.argmax(y_train, axis=1), yhat_train)
    print()

    return
 """