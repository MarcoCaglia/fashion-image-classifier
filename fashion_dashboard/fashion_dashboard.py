"""Module to House Streamlit Code for the Dashboard."""

import os
from pathlib import Path
from typing import Tuple

import pandas as pd
import streamlit as st
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource, figure
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

ROOT_DIR = Path(__file__).absolute().parent.parent \
    .joinpath(os.getenv("WORKDIR")) \
    .as_posix()

ENGINE = create_engine(
    "sqlite:///" + ROOT_DIR + "/project.db"
    )


class Dashboard:
    """Dashboarding Class, based on Streamlit."""

    def __init__(self) -> None:
        """Initialize Dashboard."""
        self.pieces_data, self.image_data = self._load_data()

    def _load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        pieces = pd.read_sql("SELECT * FROM pieces", ENGINE)
        images = pd.read_sql("SELECT * FROM images", ENGINE)

        return pieces, images

    def make_page(self) -> None:
        """Construct Webpage."""
        self._show_brand_distribution()
        self._show_average_price_by_brand()
        self._show_model_distribution_by_brand()

    def _show_brand_distribution(self):
        brand_item_count = self.pieces_data.groupby("brand") \
            .item_id.nunique() \
            .reset_index() \
            .set_index("brand") \
            .sort_values(by="item_id", ascending=False) \
            .rename(columns={"item_id": "Number of Items"}) \
            .head(25)

        st.bar_chart(brand_item_count)
        st.dataframe(brand_item_count)

    def _show_average_price_by_brand(self):
        pass

    def _show_model_distribution_by_brand(self):
        pass


if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.make_page()
