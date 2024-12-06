from plottosat import config
from plottosat.satellites import Satellite
from datetime import datetime


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
        super().__init__(config["sentinel_one"])
