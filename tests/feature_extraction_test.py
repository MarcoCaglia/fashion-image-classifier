"""Test Module for FeatureExtractor."""

import pytest
from fashion_image_classifier.feature_extraction import FeatureExtractor
from pathlib import Path
import numpy as np
from PIL import Image


IMAGES_PATHS = [
    Path("./tests/data/image_555.png"),
    Path("./tests/data/image_2500.png")
]

IMAGES = [
    Image.open(path) for path in IMAGES_PATHS
]

@pytest.fixture
def default_instance():
    default_instance = FeatureExtractor()
    return default_instance

@pytest.fixture
def default_expected_features(default_instance):
    colour_dimension = 3 if not default_instance.greyscale else 1
    expected_features = (
        default_instance.aspect_ratio[0] *
        default_instance.aspect_ratio[1] * 
        colour_dimension
    )

    return expected_features


def extract_features_from_path_test(default_instance, default_expected_features):
    images_matrix = default_instance.extract_features(
        images_paths=IMAGES_PATHS
        )

    assert isinstance(images_matrix, np.ndarray)
    assert (
        images_matrix.shape == (len(IMAGES_PATHS), default_expected_features)
        )


def extract_features_from_images_test(default_instance, default_expected_features):
    images_matrix = default_instance.extract_features(
        images=IMAGES
    )

    assert isinstance(images_matrix, np.ndarray)
    assert (
        images_matrix.shape == (len(IMAGES), default_expected_features)
        )
