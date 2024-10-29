from toml
from dataclasses import dataclass


class Satellite(dataclass):
    def __init__(self, config: dict):
        self.selected_bands = config["selected_bands"]
        self.selected_indices = config["selected_bands"]


class SentinelOne(Satellite):
    collection = "COPERNICUS/S1_GRD"
    launch_date = "2014-04-01"
    all_bands = ["", "", "", ""]

    def __init__(self, config: dict):
        super().__init__(config["sentinel_one"])()


class SentinelTwo(Satellite):
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