def do_predict(my_args):

    test_file = my_args.test_file
    if not os.path.exists(test_file):
        raise Exception("testing data file: {} does not exist.".format(test_file))
    
    model_file = get_model_filename(my_args.model_file, test_file)
    if not os.path.exists(model_file):
        raise Exception("Model file, '{}', does not exist.".format(model_file))

    X_test, y_test = load_data(my_args, test_file)
    pipeline = joblib.load(model_file)

    y_test_predicted = pipeline.predict(X_test)

    merged = X_test.index.to_frame()
    merged['SalePrice'] = y_test_predicted
    merged.to_csv("predictions.csv", index=False)

    return
