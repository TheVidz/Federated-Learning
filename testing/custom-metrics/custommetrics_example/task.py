"""custommetrics_example: A Flower / TensorFlow app for custom metrics."""

from typing import Any

import keras
import numpy as np
import tensorflow as tf
from flwr_datasets import FederatedDataset
from flwr_datasets.partitioner import IidPartitioner
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from keras import layers, models

fds = None  # Cache FederatedDataset


def load_data(
    partition_id: int, num_partitions: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load data with Flower Datasets (CIFAR-10)."""
    # Only initialize `FederatedDataset` once
    global fds
    if fds is None:
        partitioner = IidPartitioner(num_partitions=num_partitions)
        fds = FederatedDataset(
            dataset="uoft-cs/cifar10",
            partitioners={"train": partitioner},
        )
    partition = fds.load_partition(partition_id, "train")
    partition.set_format("numpy")

    # Divide data on each node: 80% train, 20% test
    partition = partition.train_test_split(test_size=0.2, seed=42)
    x_train, y_train = partition["train"]["img"] / 255.0, partition["train"]["label"]
    x_test, y_test = partition["test"]["img"] / 255.0, partition["test"]["label"]

    return x_train, y_train, x_test, y_test


def get_model(width: int = 32, height: int = 32, num_channels: int = 3) -> Any:
    
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])
    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


# Method for extra learning metrics calculation
def eval_learning(y_test, y_pred):
    """."""
    acc = accuracy_score(y_test, y_pred)
    rec = recall_score(
        y_test, y_pred, average="micro"
    )  # average argument required for multi-class
    prec = precision_score(y_test, y_pred, average="micro")
    f1 = f1_score(y_test, y_pred, average="micro")
    return acc, rec, prec, f1


def get_parameters(model):
    return model.get_weights()
