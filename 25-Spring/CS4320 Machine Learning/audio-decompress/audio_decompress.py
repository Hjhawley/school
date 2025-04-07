from open_data import load_dataset, get_datasets

X, y = load_dataset("data/train/cut/degraded", "data/train/cut/clean")
train_ds, val_ds = get_datasets(X, y, batch_size=8)
