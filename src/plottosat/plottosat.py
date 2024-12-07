from datetime import date
from typing import Union
from pathlib import Path
from ee.featurecollection import FeatureCollection

from plottosat.utils import process_date


class PlotToSat:
    """
    A class for managing and exporting satellite data collections.
    """

    def __init__(
        self,
        geometry: FeatureCollection,
        shape_file: Union[str, Path],
        start_date: Union[str, date],
        end_date: Union[str, date],
    ):
        self.geometry = geometry
        self.shape_file = Path(shape_file)
        self.start_date = process_date(start_date)
        self.end_date = process_date(end_date)


    def export_collections(self)