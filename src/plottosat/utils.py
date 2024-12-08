from typing import Union
import datetime as dt
from plottosat import logger
from ee.imagecollection import ImageCollection


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


def filter_image_collection(
    img: ImageCollection, filter_size: int, filter_shape: str
) -> ImageCollection:
    """
    Applies a median filter to an image.

    Args:
        img: The image to be filtered.
        filter_size: Size of the filter to be applied (e.g., 3 implies a 3x3 filter).
        filter_shape: Shape of the filter. Options include:
                      'circle', 'square', 'cross', 'plus', 'octagon', 'diamond'.

    Returns:
        The filtered image.
    """
    # Apply a focal median filter with the specified size and shape
    return img.focalMedian(filter_size, filter_shape, "pixels").copyProperties(
        img, ["system:time_start"]
    )
