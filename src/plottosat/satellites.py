from plottosat import logger
from datetime import date
from typing import Tuple, List, Optional
from ee.imagecollection import ImageCollection
from ee.featurecollection import FeatureCollection
from ee.computedobject import ComputedObject
from ee.geometry import Geometry
from abc import ABC, abstractmethod


class Satellite(ABC):
    """
    A base class for managing satellite data.

    Args:
        config (dict): A configuration dictionary containing settings for the satellite, including
                       selected bands and retirement date.
    """

    def __init__(
        self,
        satellite_collection: str,
        launch_date: date,
        retirement_date: Optional[date],
        bands: List[str],
    ):
        self.satellite_collection = satellite_collection
        self.launch_date = launch_date
        self.retirement_date = retirement_date
        self.bands = bands

    @abstractmethod
    def _generate_base_collection(
        self,
        start_date: date,
        end_date: date,
        geometry: Geometry | ComputedObject | FeatureCollection,
    ) -> ImageCollection:
        pass

    def get_year_start_finish_dates(self, year: int) -> Tuple[date, date]:
        """
        Get the start and finish dates for the specified year, ensuring they align with operational constraints.

        Args:
            year (int): The year for which start and finish dates are required.

        Raises:
            ValueError: If the specified year is earlier than the satellite's launch date.
            ValueError: If the specified year is later than the satellite's retirement date.

        Returns:
            Tuple[date, date]: A tuple containing the start date (January 1st) and the finish date
            (December 31st or today's date if the year is the current year).
        """
        match year:
            case year if year == date.today().year:
                logger.info(f"End date truncated to today's date: {date.today()}")
                return date(year, 1, 1), date.today()
            case year if year < self.launch_date.year:
                raise ValueError(
                    f"Start date before launch of satellite: {year} < {self.launch_date.year}"
                )
            case year if year > self.retirement_date.year:
                raise ValueError(
                    f"Start date beyond allowed operation date: {year} > {self.retirement_date.year}"
                )
            case _:
                logger.info(
                    f"Valid dates selected: {date(year, 1, 1)} \t -> \t {date(year, 12, 31)}"
                )
                return date(year, 1, 1), date(year, 12, 31)
