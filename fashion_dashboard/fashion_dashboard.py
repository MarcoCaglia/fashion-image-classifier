"""Module to House Streamlit Code for the Dashboard."""

import os
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import streamlit as st
import plotly.figure_factory as ff
from plotly import express
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
        # Add in sidebar with level selection, to drill down on brand level
        scope_selection = self._select_scope()

        # Display the KPIs according to the specified scope
        if scope_selection == "All Brands":
            self._display_general_kpi()
        else:
            self._display_drilldown(scope_selection)

    def _select_comparison_brand(self, scope_selection):
        # Present only options that are not already in scope
        options = self.pieces_data.loc[
            self.pieces_data.brand != scope_selection,
            "brand"
        ].sort_values().drop_duplicates().tolist()
        # Give also teh option of not having a comparison
        options.insert(0, "No Comparison")
        compare_brand = st.selectbox(
            "Select Brand to compare:",
            options
        )

        return compare_brand

    def _display_drilldown(self, scope_selection):
        # Give option to compare price distribution with another brand
        comparison_brand = self._select_comparison_brand(scope_selection)
        # Price Distribution of Brand
        price_distribution = self.pieces_data.loc[
            self.pieces_data.brand == scope_selection,
            "price"
            ].dropna().tolist()
        # If a comparison brand was selected, add that to the data to be
        # plotted
        if comparison_brand == "No Comparison":
            data_to_plot = [price_distribution]
            group_labels = [scope_selection]
        else:
            comparison_data = self.pieces_data.loc[
                self.pieces_data.brand == comparison_brand,
                "price"
            ].dropna().tolist()
            data_to_plot = [price_distribution, comparison_data]
            group_labels = [scope_selection, comparison_brand]

        # Make the plotly chart and display it
        price_chart = ff.create_distplot(
            data_to_plot,
            group_labels=group_labels
            )
        st.plotly_chart(price_chart)

        # Colour Distribution of Brand
        self._display_colour_distribution(scope_selection)

    def _display_colour_distribution(self, scope_selection):
        colour_distribution = self.pieces_data.loc[
            self.pieces_data.brand == scope_selection,
            ["colour", "item_id"]
        ].groupby("colour").item_id.nunique() \
            .sort_values(ascending=False) \
            .reset_index() \
            .head(50)
        colour_chart = express.bar(
            colour_distribution, x="colour", y="item_id"
            )
        st.plotly_chart(colour_chart)

    def _display_general_kpi(self):
        st.markdown(
            "# KPIs by Brand on Zalando.nl\n"
            "## Number of Items sold per Brand"
            )
        self._show_brand_distribution()
        st.markdown(
            "## Average Price per Item per Brand"
            )
        self._show_average_price_by_brand()
        st.markdown(
            "## Number of Model Photos per Item per Brand\n"
            "##### where available"
        )
        self._show_model_distribution_by_brand()

    def _select_scope(self):
        # Displayed are all brands in order of their size (descending),
        # i.e. the one with the most items should be on top
        brands = self.pieces_data.groupby("brand").item_id.nunique() \
            .sort_values(ascending=False) \
            .index \
            .tolist()
        brands.insert(0, "All Brands")
        scope_selection = st.sidebar.selectbox(
            "Choose Brand to drill down to:",
            brands
        )

        return scope_selection

    def _show_brand_distribution(self):
        # Get the number of unique item IDs per brand and display it
        # Since there are so many unique brands, many of which aren't very
        # relevant, only the 25 biggest are displayed in the graph, otherwise
        # it will be too crowded.
        brand_item_count = self.pieces_data.groupby("brand") \
            .item_id.nunique() \
            .sort_values(ascending=False)
        brand_item_count.name = "Items"

        st.bar_chart(brand_item_count.head(25))
        st.dataframe(brand_item_count)

    def _show_average_price_by_brand(self):
        # Display the average price and median price per item per brand.
        # Again, in the graph only the biggest brands are shown, otherwise it
        # would get too crowded
        price_info = self.pieces_data.groupby("brand").agg(
            {"price": [np.mean, np.median]}
        ).dropna()
        price_info.columns = ["Average Price", "Median Price"]

        # Get largest brands
        largest_brands = self.pieces_data.groupby("brand").item_id.nunique() \
            .sort_values(ascending=False) \
            .head(25) \
            .index \
            .tolist()

        # Display Mean and Median price in two different charts
        st.bar_chart(price_info.loc[largest_brands, ["Average Price"]])
        st.bar_chart(price_info.loc[largest_brands, ["Median Price"]])
        st.dataframe(price_info)

    def _show_model_distribution_by_brand(self):
        # Merge pieces and image information to be able to see images and model
        # images on brand level
        joined_information = self.image_data.merge(
            self.pieces_data, on='item_id'
            )
        # Discard, where the flag_model is not calculated
        joined_information = joined_information.loc[
            joined_information.flag_model.isin([0, 1]),
            :
            ]

        # Aggregate on Brand level
        image_information = joined_information.groupby("brand").agg(
            {"image": "nunique", "flag_model": np.sum}
        )
        image_information.columns = [
            "Number of Images", "Number of Model Images"
            ]

        # Display the KPIs
        st.bar_chart(image_information.loc[:, ["Number of Images"]])
        st.bar_chart(image_information.loc[:, ["Number of Model Images"]])


if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.make_page()
