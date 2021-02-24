"""Module to convert the labeled images in workdir to ML readable datasets."""

from fashion_image_classifier.feature_extraction import FeatureExtractor
from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split

NEGATIVES_PATHS = Path(__file__).absolute().parent \
    .joinpath("../workdir/training_images/not_worn/") \
    .glob("image_*.png")
POSITIVES_PATH = Path(__file__).absolute().parent \
    .joinpath("../workdir/training_images/worn/") \
    .glob("image_*.png")
SAVE_PATH = Path(__file__).absolute().parent.joinpath("../workdir/")


def prepare_data():
    """Use Featureextractor to convert images to data."""
    extractor = FeatureExtractor()  # Just using default settings for now.

    # Get Features and labels for negative data
    X_negative = extractor.extract_features(images_paths=NEGATIVES_PATHS)
    y_negative = np.array([0] * X_negative.shape[0])

    # Get Features and labels for positive data
    X_positive = extractor.extract_features(images_paths=POSITIVES_PATH)
    y_positive = np.array([1] * X_positive.shape[0])

    # Concatenate to single matrix/vector
    X = np.vstack([X_negative, X_positive])
    y = np.hstack([y_negative, y_positive])

    # Split the data in train and test, but keep it stratified
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.9, stratify=y
        )

    # Save to disk
    np.save(SAVE_PATH.joinpath("train_features.npy"), X_train)
    np.save(SAVE_PATH.joinpath("test_features.npy"), X_test)
    np.save(SAVE_PATH.joinpath("train_labels.npy"), y_train)
    np.save(SAVE_PATH.joinpath("test_labels.npy"), y_test)


if __name__ == "__main__":
    prepare_data()
