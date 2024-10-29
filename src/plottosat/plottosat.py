import pandas as pd
from datetime import date
from plottosat import config, logger
from typing import Union
from pathlib import Path
from ee.featurecollection import FeatureCollection
from datetime import datetime, date

from plottosat.satellites import SentinelOne, SentinelTwo
from plottosat.polygons import Polygons
from plottosat.field_data import FieldData


class PlotToSat:
    """A class for managing and exporting satellite data collections."""

    def __init__(self,
                  geometry: FeatureCollection, 
                  shape_file: Union[str, Path], 
                  year: int):
        """Initialize PlotToSat with necessary parameters and setup.

        Args:
            geometry (dict): Geometric information for satellite data collection.
            shape_file (dict or str): Properties for the field data or shapefile path.
            year (int): Year of interest for data export.
        """
        self.sampling_size = 400
        self.sample_count = 0
        self.max_size = 0
        self.csv_df = None
        self.year = year
        self.shape_file = Path(shape_file)
        self.shape_polygons = self.load_polygons(self.shape_file)
        self.shp_pol_key_col = None
        self.filedata_file_with_ids = "fieldDataWithIdentifiers/FieldDataWithIdentifiers.csv"
        self.today_date = date.today()
        self.sentinel_one = SentinelOne()
        self.sentinel_two = SentinelTwo()
        self.geometry = geometry
        self.masks = {}

    @staticmethod
    def load_polygon(file_path: Path) -> Polygons:
        return Polygons(file_path, config["polygons"]["key_column"])

    def add_field_data(self, properties):
        """Add field data to the manager.

        Args:
            properties (dict): Properties including csv filename, projection, and year label.
        """
        self.csv_df = FieldData(properties)
        self.max_size = self.csv_df.get_len()

    def set_sampling(self, new_sampling):
        """Set the sampling limit for plot data to avoid processing all at once.

        Args:
            new_sampling (int): New sampling size.
        """
        self.sampling_size = new_sampling
        if self.shape_file is not None:
            self.shp_polygons.set_sampling(new_sampling)
        logger.info(f"sampling size updated: {self.sampling_size}")

    def set_masks(self, new_masks):
        """Set masks for data collection.

        Args:
            new_masks (dict): Masks to be applied.
        """
        self.masks = new_masks

    def add_collection(self, collection_name):
        """Add a new collection to the system.

        Args:
            collection_name (str): Name of the collection to add.
        """
        self.number_of_available_cols += 1
        self.list_of_available_collections.append(collection_name)