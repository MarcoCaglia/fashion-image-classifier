# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import re

import pandas as pd
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
import numpy as np


class SourcingPipeline:

    CLOTHING_COLUMNS = (
        "item_id",
        'name',
        "brand",
        "price",
        "colour",
        "url",
        "reviews",
        "rating"
        )
    IMAGE_COLUMNS = ("item_id", "image")

    def __init__(self, workdir):
        self.workdir = workdir

        self.engine = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            workdir=crawler.settings.get("WORKDIR")
        )

    def open_spider(self, spider):
        # Assert that directory exists
        if not self.workdir.is_dir():
            raise AssertionError("Workdir does not exist.")

        # Open connectionto DB
        self.engine = create_engine(
            f"sqlite:///{self.workdir.as_posix()}/project.db"
        )

    def process_item(self, item, spider):
        # Unpack clothing data and images for upload in two different DB tables
        data = pd.DataFrame(dict(item))
        clothing_data = data.loc[:, SourcingPipeline.CLOTHING_COLUMNS].copy() \
            .drop_duplicates()
        image_data = data.loc[:, SourcingPipeline.IMAGE_COLUMNS].copy() \
            .drop_duplicates()
        image_data["flag_model"] = -1  # Signifies that this image has not
        # been labeled yet.

        # Apply parsing steps to the individual tables
        self.apply_clothing_parsing(clothing_data)
        self.apply_images_parsing(image_data)

        # Load to database
        clothing_data.to_sql(
            "pieces",
            con=self.engine,
            if_exists="append",
            index=False
        )

        image_data.to_sql(
            "images",
            con=self.engine,
            if_exists="append",
            index=False
        )

    def apply_clothing_parsing(self, clothing_data):
        clothing_data = self.parse_price(clothing_data)
        clothing_data = self.parse_reviews(clothing_data)
        clothing_data.rating = clothing_data.rating.astype(float)

        return clothing_data

    def parse_reviews(self, clothing_data):
        integer_pattern = re.compile(r"\d+")
        clothing_data.reviews = clothing_data.reviews.map(
            lambda reviews: re.findall(integer_pattern, reviews)[0]
            if re.search(integer_pattern, str(reviews))
            else np.NaN
        )

        return clothing_data

    def parse_price(self, clothing_data):
        price_pattern = re.compile(r"\d+[,\.]\d+")

        def extract_price(price):
            if re.search(price_pattern, str(price)):
                price = re.findall(price_pattern, str(price))[-1]
                price = float(price.replace(",", "."))

            else:
                price = np.NaN

            return price

        clothing_data.price = clothing_data.price.apply(
            extract_price
            )

        return clothing_data

    def apply_images_parsing(self, image_data):
        return image_data
