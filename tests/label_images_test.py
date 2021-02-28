"""Test Module for ImageLabeler."""

import pytest
from fashion_image_classifier.label_images import ImageLabeler
import numpy as np

IMAGES = [
    'https://img01.ztat.net/article/spp-media-p1/90eaa44056f43c25bf7df2c8093485fc/e00bafbb57e34cfe87b081b936e37c1d.jpg?imwidth=156&filter=packshot',
    'https://img01.ztat.net/article/spp-media-p1/4e66fa243a3c394a9890146115c4e996/a17bca0a169243218c13979783159ddd.jpg?imwidth=156',
    'https://img01.ztat.net/article/spp-media-p1/0c57a1bcf925472085cc512955710b47/912ba13c1a8043b1b8cca6c347fd1485.jpg?imwidth=762',
    'https://img01.ztat.net/article/spp-media-p1/3409faffd857322c91bbf67956ad541a/53a21af910a543529d09847d55525436.jpg?imwidth=156',
    'https://img01.ztat.net/article/spp-media-p1/5055e3652a34398fa201134b6765f7a9/3c56f233910648edbca776bf9074e364.jpg?imwidth=156',
    'https://img01.ztat.net/article/spp-media-p1/0c41f71d1a46465e9078aa80772c0799/53739bc75c214b42975e770777d7d4f9.jpg?imwidth=156',
    'https://img01.ztat.net/article/spp-media-p1/4bb95d2e06813b59be3d05cdaeb3c779/ce2d804e64fc4f4fb80a0d4417f0c5d4.jpg?imwidth=762',
    'https://img01.ztat.net/article/spp-media-p1/c1e7626242b43651a715fc06d570af0a/332639308b4c415997f07f04806e812d.jpg?imwidth=156',
    'https://img01.ztat.net/article/spp-media-p1/1cfe54e877b23aad96017e7408703b0b/9304e679dc53490dabeeae64ca108ec3.jpg?imwidth=156',
    'https://img01.ztat.net/article/spp-media-p1/9b4ab1c1e34b3115b754a1311765edd4/3cff6e540916488488c38fb9d3f5397a.jpg?imwidth=762'
]

EXPECTED = dict(zip(IMAGES, [1] * len(IMAGES)))


class TestModel:
    def predict(self, X):
        return np.array([1] * len(X))


@pytest.fixture
def test_model():
    return TestModel()


@pytest.fixture
def default_instance(test_model):
    return ImageLabeler(model=test_model)


def label_images_expected_output(default_instance):
    actual = default_instance.label_images(IMAGES)

    assert actual == EXPECTED
