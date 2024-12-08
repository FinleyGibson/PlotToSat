import numpy as np
from plottosat import config, logger
from plottosat.utils import process_date, filter_image_collection
from plottosat.satellites import Satellite
from datetime import date
from ee.geometry import Geometry
from ee.featurecollection import FeatureCollection
from ee.computedobject import ComputedObject
from ee.imagecollection import ImageCollection
from ee.filter import Filter
from typing import Union, Dict, List


class SentinelOne(Satellite):
    """
    A class for managing Sentinel-1 satellite data.

    Inherits from Satellite and provides specific configurations for Sentinel-1.

    Attributes:
        collection (str): The data collection identifier for Sentinel-1.
        launch_date (str): The launch date of the Sentinel-1 satellite.
        all_bands (list): List of all available bands for Sentinel-1.
    """

    satellite_collection = "COPERNICUS/S1_GRD"
    launch_date = date(2014, 4, 1)
    bands = ["VVAsc", "VHAsc", "VVDes", "VHDes"]
    retirement_date = (
        process_date(config["sentinel_one"]["retirement_date"])
        if config["sentinel_one"]["retirement_date"] != ""
        else date.today()
    )

    def __init__(self):
        super().__init__(
            satellite_collection=self.satellite_collection,
            launch_date=self.launch_date,
            retirement_date=self.retirement_date,
            bands=self.bands,
        )

    def _generate_base_collection(
        self,
        start_date: Union[str, date],
        end_date: Union[str:date],
        geometry: Geometry | ComputedObject | FeatureCollection,
    ) -> ImageCollection:
        start_date = max(process_date(start_date), self.launch_date)
        end_date = min(process_date(end_date), self.retirement_date)
        return (
            ImageCollection(self.satellite_collection)
            .filterDate(start_date, end_date)
            .filterBounds(geometry)
            .filter(Filter.listContains("transmitterReceiverPolarisation", "VV"))
            .filter(Filter.listContains("transmitterReceiverPolarisation", "VH"))
            .filter(Filter.eq("instrumentMode", "IW"))
        )

    def get_bands(
        self, base_collection: ImageCollection, selected_bands: List[str]
    ) -> Dict[str, ImageCollection]:
        # check for valid band selection
        if not np.all([band in self.bands for band in selected_bands]):
            logger.error(
                f"Bands selected for {self.__class__.__name__} are not valid.\n"
                f"Expected:\n{self.bands}\n\n"
                f"Received:\n{selected_bands}"
            )
            raise ValueError(f"Bad band selection for {self.__class__.__name__}")

        out_bands = {}

        for band_name in selected_bands:
            polarity = band_name[:2]

            match band_name[2:]:
                case "Asc":
                    direction = "ASCENDING"
                case "Des":
                    direction = "DESCENDING"
                case _:
                    logger.error(
                        f"band name: {band_name} not recognised for {self.__class__.__name__}. Should be '**Asc' or '**Des'"
                    )
                    raise ValueError

            out_bands[band_name] = (
                base_collection.filter(Filter.eq("orbitProperties_pass", direction))
                .select(polarity)
                .map(
                    lambda img: filter_image_collection(
                        img, filter_size=3, filter_shape="circle"
                    )
                )
            )

        return out_bands
