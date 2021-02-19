"""Module to run model training after prepare.py has been run."""

from pathlib import Path

import numpy as np
import yaml
from joblib import dump
from sklearn.decomposition import KernelPCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from scripts.prepare import SAVE_PATH

X_TRAIN_PATH = SAVE_PATH.joinpath("train_features.npy")
Y_TRAIN_PATH = SAVE_PATH.joinpath("train_labels.npy")

PARAMS_PATH = Path(__file__).absolute().parent.parent.joinpath('params.yaml')


def train_model():
    """Train the model."""
    X_train = np.load(X_TRAIN_PATH)
    y_train = np.load(Y_TRAIN_PATH)

    with PARAMS_PATH.open("r") as f:
        params = yaml.safe_load(f)["train"]

    model = Pipeline([
        (
            "scaler",
            StandardScaler() if params["use_scaler"] else "passtrhough"
            ),
        ("pca", KernelPCA(
            n_components=params["pca__n_components"],
            gamma=params["pca__gamma"],
            kernel=params["pca__kernel"]
            )
            if params["use_pca"] else "passthrough"),
        ("classifier", SVC(
            C=params["classifier__C"],
            kernel=params["classifier__kernel"],
            gamma=params["classifier__gamma"]
            ))
    ])

    _ = model.fit(X_train, y_train)

    _ = dump(model, SAVE_PATH.joinpath("model.joblib"))


if __name__ == "__main__":
    train_model()
