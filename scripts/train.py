"""Module to run model training after prepare.py has been run."""

from .prepare import SAVE_PATH
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import Decomposition

X_TRAIN_PATH = SAVE_PATH.joinpath("train_features.npy")
y_TRAIN_PATH = SAVE_PATH.joinpath("train_labels.npy")
X_TEST_PATH = SAVE_PATH.joinpath("test_features.npy")
y_TEST_PATH = SAVE_PATH.joinpath("test_labels.npy")


def train_model():
    """Train the model."""
    X_train = np.load(X_TRAIN_PATH)
    y_train = np.load(y_TRAIN_PATH)
    X_test = np.load(X_TEST_PATH)
    y_test = np.load(y_TEST_PATH)

    model = Pipeline([
        ("scaler", StandardScaler() if use_)
    ])
