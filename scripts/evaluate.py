"""Module to evaluate the previously trained model."""

import numpy as np
import pandas as pd
from joblib import load
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)
import seaborn as sns

from scripts.prepare import SAVE_PATH

X_TEST_PATH = SAVE_PATH.joinpath("test_features.npy")
Y_TEST_PATH = SAVE_PATH.joinpath("test_labels.npy")

MODEL_PATH = SAVE_PATH.joinpath("model.joblib")


def evaluate():
    """Evaluate the model."""
    X_test = np.load(X_TEST_PATH)
    y_test = np.load(Y_TEST_PATH)

    model = load(MODEL_PATH)

    y_hat = model.predict(X_test)

    metrics = {
        "Accuracy": accuracy_score(y_test, y_hat),
        "Precision": precision_score(y_test, y_hat),
        "Recall": recall_score(y_test, y_hat),
        "F1-Score": f1_score(y_test, y_hat),
    }

    metrics = pd.DataFrame.from_dict(
        metrics, orient="index", columns=["Test-Score"]
        )
    metrics.to_csv(SAVE_PATH.joinpath("model_test_results.csv"))

    confusion = sns.heatmap(confusion_matrix(y_test, y_hat), annot=True)
    confusion.figure.savefig(SAVE_PATH.joinpath("model_test_confusion.png"))


if __name__ == "__main__":
    evaluate()
