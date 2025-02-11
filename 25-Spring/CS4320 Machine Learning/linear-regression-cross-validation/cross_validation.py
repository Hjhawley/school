def do_cross(my_args):
    train_file = my_args.train_file
    if not os.path.exists(train_file):
        raise Exception("training data file: {} does not exist.".format(train_file))

    X, y = load_data(my_args, train_file)

    pipeline = make_SGD_fit_pipeline(my_args)

    cv_results = sklearn.model_selection.cross_validate(
        pipeline, X, y, 
        cv=5,  # 5 folds? see how many i can do
        n_jobs=-1, 
        verbose=3, 
        scoring=('r2', 'neg_mean_squared_error', 'neg_mean_absolute_error')
    )

    print("R2:", cv_results['test_r2'], cv_results['test_r2'].mean())
    print("MSE:", cv_results['test_neg_mean_squared_error'], cv_results['test_neg_mean_squared_error'].mean())
    print("MAE:", cv_results['test_neg_mean_absolute_error'], cv_results['test_neg_mean_absolute_error'].mean())
