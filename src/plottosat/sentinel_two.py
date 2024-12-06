from plottosat.satellites import Satellite
from plottosat import config
from datetime import datetime


class SentinelTwo(Satellite):
    """
    A class for managing Sentinel-2 satellite data.

    Inherits from Satellite and provides specific configurations for Sentinel-2.

    Attributes:
        collection (str): The data collection identifier for Sentinel-2.
        launch_date (str): The launch date of the Sentinel-2 satellite.
        all_bands (list): List of all available bands for Sentinel-2.
    """

    collection = "COPERNICUS/S2_SR_HARMONIZED"
    launch_date = datetime.strptime("2015-05-23", "%Y-%H-%d").date()
    all_bands = [
        "B1",
        "B2",
        "B3",
        "B4",
        "B5",
        "B6",
        "B7",
        "B8",
        "B8A",
        "B9",
        "B11",
        "B12",
    ]

    def __init__(self):
        super().__init__(config["sentinel_two"])
        self.clouds = self.config["clouds"]
