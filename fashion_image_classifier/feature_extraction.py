"""Module to extract Features from Images."""

import numpy as np
from PIL import Image
import PIL
from typing import Tuple, List
from PIL.PngImagePlugin import PngImageFile


class FeatureExtractor:
    """Class for extracting Features from Images."""

    def __init__(
        self,
        greyscale: bool = False,
        aspect_ratio: Tuple[int, int] = (256, 256),
        feature_shape: Tuple[int, int] = (1, -1)
    ) -> None:
        """Initialize Feature Extractor.

        Args:
            greyscale (bool, optional): If set to True, the images will be in
                greyscale, without colours. Defaults to False. TODO
            aspect_ration (Tuple[int, int], optional): If specified, the aspect
                ratio will be addjusted to the passed shape. Defaults to
                (256, 256).
            feature_shape (Tuple[int, int]): Output shape of the features of
                the individual images. The daufault value of (1, -1) will
                return one row per image, which as many columns as is needed to
                accomodate the aspect ratio. Defaults to (1, -1).
        """
        self.greyscale = greyscale
        self.aspect_ratio = aspect_ratio
        self.feature_shape = feature_shape

    def extract_features(
        self,
        images: List[PngImageFile] = [],
        images_paths: List[str] = []
    ):
        """Extract Features from images.

        Accepts either a list of pre-loaded images or a list of paths, but
        not both at the same time.

        Args:
            - images (List[Image], optional): List of loaded images. Defaults
                to [].
            -images_paths (List[str], optional): List of paths to images
        """
        # First check if the parameters have been correctly passed
        self._check_parameters(images, images_paths)

        # If paths are used, load the images lazily to save memory
        if images_paths:
            images = self._load_images_lazily(images_paths)

        # If an aspect ratio was specified, apply it (lazily) to the images
        if self.aspect_ratio:
            images = self._rescale_images(images)

        # This method will evaluate the images and put them to gether in a
        # single numerical matrix.
        features = self._images_to_data(images)

        return features

    @staticmethod
    def _check_parameters(images, images_paths):
        # Exactly one of the parameters should be passed, the other not
        images_passed = bool(images)
        paths_passed = bool(images_paths)

        # If not exactly one of teh above is true, raise an error
        if sum([images_passed, paths_passed]) != 1:
            raise AssertionError(
                "Please pass exactly one of images or images_paths."
                )

    @staticmethod
    def _load_images_lazily(paths):
        # Iterate over paths and return a generator for lazy evluation
        for path in paths:
            image = Image.open(path)
            yield image

    def _rescale_images(self, images):
        # Apply the resizing (lazily) to each image
        for image in images:
            image = image.resize(self.aspect_ratio)
            yield image

    def _images_to_data(self, images):
        # Evaluate all images and shape the resultting vectors in the specified
        # shape.
        image_vectors = [
            np.array(image).reshape(self.feature_shape)
            for image
            in images
            ]

        # Concatenate the image vectors to as single matrix
        feature_matrix = np.vstack(image_vectors)

        return feature_matrix
