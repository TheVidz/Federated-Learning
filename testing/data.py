from tensorflow.keras.datasets import cifar10
import numpy as np

def load_data():
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize data
    return (x_train, y_train), (x_test, y_test)

def split_data(x, y, num_clients):
    data_per_client = len(x) // num_clients
    x_splits = [x[i * data_per_client: (i + 1) * data_per_client] for i in range(num_clients)]
    y_splits = [y[i * data_per_client: (i + 1) * data_per_client] for i in range(num_clients)]
    return x_splits, y_splits
