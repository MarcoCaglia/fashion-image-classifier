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
            .sort_values(ascending=False) \
            .reset_index() \
            .head(50)
        cds = ColumnDataSource(brand_item_count)
        tooltip = HoverTool
        plot = figure(
            title="Items per Brand",
            tools="pan,box_zoom,reset,save",
            y_axis_label="Number of Item",
            x_axis_label="Brand",
            x_range=brand_item_count.brand.tolist()
        )

        plot.vbar(
            x="brand",
            top="item_id",
            source=cds
            )

        st.bokeh_chart(plot, use_container_width=True)

    def _show_average_price_by_brand(self):
        pass

    def _show_model_distribution_by_brand(self):
        pass


if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.make_page()
