"""Helper Module for labeling images in a jupyter notebook."""

import hashlib
from io import BytesIO
from pathlib import Path
from typing import Iterable, List

import numpy as np
import pandas as pd
import PIL
import requests
from IPython.display import display
from pigeon import annotate
from PIL import Image


class ImageLabeler:
    """Helper Class for labeling images in a jupyter notebook."""

    def __init__(self, urls: Iterable[str], save_path: str) -> None:
        """Initialize Imagelabeler.

        Args:
            urls (List[str]): URLs from which to load the images to be labeled.
            save_path (str): location to safe the labeled images to. Must be a
            folder in which sibfolders can be created for each class.
        """
        # Get all scraped image URLs (shuffling to no get items in order)
        self.images = urls
        np.random.shuffle(self.images)

        # Assign a unique identifier to each URL. This will be the filenames of
        # the labeled images later.
        self._get_image_identifiers()

        self.save_path = Path(save_path).absolute()

        # Raise an exception if the passed save_path does not exist
        if not self.save_path.is_dir():
            raise AssertionError("Save_path is not a location.")

        # In this empty list, the downloaded images will be stored until the
        # user writes them to disk.
        self.actual_images: List[PIL.Image] = []

    def _get_image_identifiers(self):
        # The unique identifier for each image (URL) will be the hashed URL, To
        # make sure that the same image is always stored in the same file, to
        # avoid duplicates.
        hashed_urls = [
            hashlib.sha256(url.encode("utf-8")).hexdigest()
            for url in self.images
        ]

        self.images = tuple(zip(self.images, hashed_urls))

    def label_images(self, options: List[str] = ["Worn", "Not Worn"]):
        """Label images loaded from DB.

        Args:
            options (list, optional): Potential Labels. Defaults to ["Worn",
                "Not Worn"].
        """
        # Options will be standardized to an extent to make the save_paths for
        # the labeled images easier to read.
        standardized_options = [
            option.lower().replace(" ", "_") for option in options
            ]

        # First, check if each option has a subfolder in the save_path-folder.
        self._check_subclass_folders_exist(standardized_options)

        # Get all previously labeled images to make sure they are not labeled
        # again.
        labeled_images_hashes = []
        for option in standardized_options:
            subclass_path = self.save_path.joinpath(option).glob('*.png')
            labeled_images_hashes += [
                file.absolute().as_posix().split("/")[-1].replace(".png", "")
                for file
                in subclass_path
                ]
        self.images = filter(
            lambda image: image[1] not in labeled_images_hashes, self.images
            )

        # Present Annotation
        self.annotated = annotate(
            self.images,
            options=standardized_options,
            display_fn=self._display_image
        )

    def save_images(self):
        """Save images to disk for further processing.

        The location of each image is determined by the passed save_path and
        the label on the image. Can be done at any time, even when labeling is
        still in progress.
        """
        # Use the label and url_hash from the annotated URLs, alongside the
        # actual images (downloaded and stored during annotation) to write
        # the results to disk.
        for index, labeled_images in enumerate(self.annotated):
            path = self.save_path.joinpath(labeled_images[1]) \
                .joinpath(labeled_images[0][1] + ".png")
            self.actual_images[index].save(path)

    def _check_subclass_folders_exist(self, standardized_options):
        # For every option, make sure there is already a folder for it, 
        # ootherwise create that folder.
        for option in standardized_options:
            option_path = self.save_path.joinpath(option)
            if not option_path.is_dir():
                option_path.mkdir()

    def _display_image(self, url_id):
        # This code requests the data from the image url and presents it to the
        # User for labeling.
        url = url_id[0]
        byte_response = requests.get(url)
        image = Image.open(BytesIO(byte_response.content))
        self.actual_images.append(image)
        display(image)
