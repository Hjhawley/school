from open_data import load_dataset, get_datasets
from model_creation import create_model

class Args:
    model_name = "a"

X, y = load_dataset("data/train/cut/degraded", "data/train/cut/clean")
train_ds, val_ds = get_datasets(X, y, batch_size=8)

model = create_model(Args(), input_shape=X[0].shape)
model.fit(train_ds, validation_data=val_ds, epochs=1)
