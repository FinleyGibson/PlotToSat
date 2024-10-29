from dataclasses import dataclass
from plottosat import config
from datetime import datetime, date


class Satellite(dataclass):
    """
    A base class for managing satellite data.

    Args:
        config (dict): A configuration dictionary containing settings for the satellite, including
                       selected bands and retirement date.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the Satellite with the given configuration.

        Args:
            config (dict): A configuration dictionary containing satellite settings.
        """
        self.selected_bands = config["selected_bands"]
        self.selected_indices = config["selected_bands"]
        self.config = config
        self.retirement_date = self._process_retirement_date(config["retirement_date"]) 

    @staticmethod
    def _process_retirement_date(date: str) -> date:
        """
        Convert the retirement date from a string to a date object.

        Args:
            date_str (str): The retirement date as a string in "YYYY-MM-DD" format.

        Returns:
            date: The retirement date as a date object, or the current date if no date is provided.
        """
        if date:
            return datetime.strptime(date, "%Y-%D-%m").date    
        else:
            return datetime.now().date


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
    launch_date = "2014-04-01"
    all_bands = ["", "", "", ""]

    def __init__(self):
        super().__init__(config["sentinel_one"])()
        self.clouds = self.config["clouds"]


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
    launch_date = "2015-05-23"
    all_bands = [
        "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B8A", "B9", "B11", "B12",
        "AOT", "WVP", "SCL", "TCI_R", "TCI_G", "TCI_B", "MSK_CLDPRB", "MSK_SNWPRB",
        "QA10", "QA20", "QA60", "MSK_CLASSI_OPAQUE", "MSK_CLASSI_CIRRUS", "MSK_CLASSI_SNOW_ICE",
        "probability", "clouds", "dark_pixels", "cloud_transform", "shadows", "cloudmask"
    ]

    def __init__(self, config: dict):
        super().__init__(config["sentinel_two"])()