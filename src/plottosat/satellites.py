from dataclasses import dataclass
from plottosat import config, logger
from datetime import datetime, date
from typing import Tuple


@dataclass
class Satellite:
    """
    A base class for managing satellite data.

    Args:
        config (dict): A configuration dictionary containing settings for the satellite, including
                       selected bands and retirement date.
    """

    launch_date: date = None

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
            return datetime.strptime(date, "%Y-%D-%m").date()
        else:
            return datetime.now().date()

    def get_start_finish_dates(self, year: int) -> Tuple[date, date]:
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
