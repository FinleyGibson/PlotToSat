from plottosat import config
from plottosat.utils import process_date
from plottosat.satellites import Satellite
from datetime import datetime, date
from ee.geometry import Geometry
from ee.featurecollection import FeatureCollection
from ee.computedobject import ComputedObject
from ee.imagecollection import ImageCollection
from ee.filter import Filter
from typing import Union


class SentinelOne(Satellite):
    """
    A class for managing Sentinel-1 satellite data.

    Inherits from Satellite and provides specific configurations for Sentinel-1.

    Attributes:
        collection (str): The data collection identifier for Sentinel-1.
        launch_date (str): The launch date of the Sentinel-1 satellite.
        all_bands (list): List of all available bands for Sentinel-1.
    """

    collection = "COPERNICUS/S1_GRD"
    launch_date = datetime.strptime("2014-04-01", "%Y-%H-%d").date()
    bands = ["VVAsc", "VHAsc", "VVDes", "VHDes"]

    def __init__(self):
        super().__init__(
            collection=self.collection,
            launch_date=self.launch_date,
            retirement_date=self._process_retirement_date(
                config["sentinel_one"]["retirement_date"]
            ),
            bands=self.bands,
            selected_bands=config["sentinel_one"]["selected_bands"],
        )

    def generate_image_collection(
        self,
        start_date: Union[str, date],
        end_date: Union[str:date],
        geometry: Geometry | ComputedObject | FeatureCollection,
    ) -> ImageCollection:
        start_date = process_date(start_date)
        end_date = process_date(end_date)
        return (
            ImageCollection(self.collection)
            .filterDate(start_date, end_date)
            .filterBounds(geometry)
            .filter(Filter.listContains("transmitterReceiverPolarisation", "VV"))
            .filter(Filter.listContains("transmitterReceiverPolarisation", "VH"))
            .filter(Filter.eq("instrumentMode", "IW"))
        )
