from dataclasses import dataclass
from plottosat import logger
from datetime import datetime, date
from typing import Tuple, List


@dataclass
class Satellite:
    """
    A base class for managing satellite data.

    Args:
        config (dict): A configuration dictionary containing settings for the satellite, including
                       selected bands and retirement date.
    """

    def __init__(
        self,
        collection: str,
        launch_date: date,
        retirement_date: date,
        bands: List[str],
        selected_bands: List[str],
    ):
        self.collection = collection
        self.launch_date = launch_date
        self.retirement_date = retirement_date
        self.bands = bands
        self.selected_bands = selected_bands

    @staticmethod
    def _process_retirement_date(date: str) -> date:
        """
        Convert the retirement date from a string to a date object.

        Args:
            date_str (str): The retirement date as a string in "YYYY-MM-DD" format.

        Returns:
            date: The retirement date as a date object, or the current date if no date is provided.
        """
        try:
            date = datetime.strptime(date, "%Y-%D-%m").date()
            return date
        except ValueError:
            today = datetime.now().date()
            if date == "":
                logger.info(
                    "No retirement date for {self.__class__.__name__}. Limit set to today: {today}."
                )
            else:
                logger.info(
                    "Retirement date {date} for {self.__class__.__name__} note recognised. Limit set to today: {today}."
                )

            return today

    def get_start_finish_dates(self, year: int) -> Tuple[date, date]:
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
