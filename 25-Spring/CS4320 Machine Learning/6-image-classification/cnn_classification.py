#!/usr/bin/env python3
#

import sys
import argparse
import logging
import os.path

import joblib
import tensorflow as tf
import keras
#tf.debugging.set_log_device_placement(True) # make sure i'm using cuda

import open_data
import model_creation

################################################################
#
# CNN functions
#
def do_cnn_fit(my_args):
    """
    Create a new model, and fit it to the training data.
    """
    X, y = open_data.load_batch(my_args.batch_number)
    model = model_creation.create_model(my_args, X.shape[1:])
    early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    history = model.fit(X, y, epochs=10, verbose=1, callbacks=[early_stopping], validation_split=0.2, shuffle=True, batch_size=32)
    model_file = my_args.model_file
    joblib.dump(model, model_file)
    joblib.dump(history.history, "{}.history".format(model_file))
    return

def do_cnn_refit(my_args):
    X, y = open_data.load_batch(my_args.batch_number)
    model_file = my_args.model_file
    model = joblib.load(model_file)
    early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    history = model.fit(X, y, epochs=10, verbose=1, callbacks=[early_stopping], validation_split=0.2, shuffle=True, batch_size=32)
    joblib.dump(model, model_file)
    joblib.dump(history.history, "{}.history".format(model_file))
    return
#
# CNN functions
#
################################################################

################################################################
#
# Evaluate existing models functions
#
import model_evaluation
import model_history
#
# Evaluate existing models functions
#
################################################################



def parse_args(argv):
    parser = argparse.ArgumentParser(prog=argv[0], description='Image Classification with CNN')
    parser.add_argument('action', default='cnn-fit',
                        choices=[ "cnn-fit", "score", "learning-curve", "cnn-refit" ], 
                        nargs='?', help="desired action")

    parser.add_argument('--batch-number',  '-b', default=1,     type=int,   help="which training batch to use (default=1)")
    parser.add_argument('--model-file',    '-m', default="model.joblib",    type=str,   help="name of file for the model (default is constructed from train file name when fitting)")
    parser.add_argument('--model-name',    '-M', default="v",    type=str,   help="name of model create function")

    my_args = parser.parse_args(argv[1:])

    #
    # Do any special fixes/checks here
    #
    
    return my_args


def main(argv):
    my_args = parse_args(argv)
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.WARN)

    if my_args.action == 'cnn-fit':
        do_cnn_fit(my_args)
    elif my_args.action == 'cnn-refit':
        do_cnn_refit(my_args)
    elif my_args.action == 'score':
        model_evaluation.show_score(my_args)
    elif my_args.action == 'learning-curve':
        model_history.plot_history(my_args)
    else:
        raise Exception("Action: {} is not known.".format(my_args.action))

    return

if __name__ == "__main__":
    main(sys.argv)

    
