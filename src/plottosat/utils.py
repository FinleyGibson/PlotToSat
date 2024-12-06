from typing import Union
import datetime as dt
from plottosat import logger


def process_date(date: Union[str, dt.date]) -> dt.date:
    if isinstance(date, dt.date):
        return date
    else:
        try:
            date = date.replace("/", "-").replace(".", "-")
            return dt.datetime.strptime(date, "%Y-%M-%d")
        except ValueError as e:
            logger.error(
                f"date: {date} of invalid format, should be in format: %Y-%M-%d"
            )
            raise e
