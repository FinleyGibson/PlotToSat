import ee

def addBuffer (image, buffer):
    """
    Adds a buffer around a given raster

    image: imported raster to be buffered 
    buffer: number of meters to add around the given raster
    """
    if buffer == 0:
        return image
    else:
        return ee.Image(1).cumulativeCost(image, buffer, True)
  
def addBufferRename (image, buffer, name):
    """
    adds a buffer around a given raster

    buffer: number of meters to add around the given raster
    imgName: the new name of the image # otherwise the name of the bands is "cumulative_cost"
    """
    if buffer == 0:
       return image.rename(name)
    else:
        return ee.Image(1).cumulativeCost(image, buffer, True).rename(name)
  
  
def filterSpeckles3x3(img):
    """
    Apply a circular median filter with a kernel size of 3x3 to the input image.

    Parameters:
    img: The image to be filtered.

    Returns:
    The filtered image.
    """
    # Apply a focal median filter
    return img.focalMedian(3, 'circle', 'pixels').copyProperties(img, ['system:time_start'])


def filterSpeckles(img, filterSize, filterShape):
    """
    Apply a median filter to the input image with specified size and shape.

    Parameters:
    img: The image to be filtered.
    filterSize: The size of the filter to be applied (e.g., 3 for a 3x3 filter).
    filterShape: The shape of the filter. Options include:
        - 'circle'
        - 'square'
        - 'cross'
        - 'plus'
        - 'octagon'
        - 'diamond'

    Returns:
    The filtered image.
    """
    # Apply a focal median filter
    return img.focalMedian(filterSize, filterShape, 'pixels').copyProperties(img, ['system:time_start'])


## TODO: figure out of this is actually needed as it currently returns None
# def byMonth (col):
#   months = ee.List.sequence(1, 12)


def monthly_avg(collection, years, months):
    """
    Calculate monthly averages for a given image collection.

    This function filters the collection for each specified year and month,
    computes the mean image for that month, and returns an ImageCollection 
    of the monthly averages.

    Parameters:
    collection (ee.ImageCollection): The image collection to be averaged.
    years (list): A list of years for which to compute the averages.
    months (list): A list of months for which to compute the averages.

    Returns:
    ee.ImageCollection: An ImageCollection containing the monthly average images.
    """
    avg = []
    for year in years:
        for month in months:
            print("Processing month...")
            monthly_avg = (collection.filter(ee.Filter.calendarRange(year, year, 'year'))
                                 .filter(ee.Filter.calendarRange(month, month, 'month'))
                                 .mean()
                                 .set({'month': month, 'year': year}))
            avg.append(monthly_avg)
    return ee.ImageCollection.fromImages(avg)


def remove_period_from_collection(col, start, end):
    """
    Remove a specified period from an image collection.

    This method filters the collection to exclude images from the specified date range.

    Parameters:
    col (ee.ImageCollection): The image collection to filter.
    start (str): The start date of the bad period (format 'YYYY-MM-DD').
    end (str): The end date of the bad period (format 'YYYY-MM-DD').

    Returns:
    ee.ImageCollection: The filtered image collection without the specified period.
    """
    bad_data_filter = ee.Filter.date(start, end)
    new_col = col.filter(bad_data_filter.Not())
    return new_col


def get_year_month_or_day(date, what):
    """
    Extract year, month, or day from a date string.

    Parameters:
    date (str): The date in the form 'YYYY-MM-DD'.
    what (str): The component to extract ('year', 'month', 'day').

    Returns:
    int: The extracted value, or None if the input is invalid.
    """
    my_list = date.split("-")
    if what == 'year':
        return int(my_list[0])
    elif what == 'month':
        return int(my_list[1])
    elif what == 'day':
        return int(my_list[2])
    else:  # Invalid input
        return None


def by_month(i_year, col):
    """
    Create a collection of monthly average images for a specified year.

    Each image in the returned collection represents the pixelwise average 
    for a corresponding calendar month.

    Parameters:
    i_year (int): The year of interest.
    col (ee.ImageCollection): The image collection to be filtered.

    Returns:
    ee.ImageCollection: A collection of 12 images, one for each month.
    """
    start_date = ee.Date.fromYMD(i_year, 1, 1)
    end_date = start_date.advance(1, 'year')
    tmp_col = col.filter(ee.Filter.date(start_date, end_date))
    return ee.ImageCollection.fromImages(ee.List([
        (tmp_col.filter(ee.Filter.calendarRange(i, i, 'month')).mean().set('month', i))
        for i in range(1, 13)
    ]))


def remove_period(start_date, end_date, col):
    """
    Remove a specified period from an image collection.

    Parameters:
    start_date (str): The starting date of the period to be removed (format 'YYYY-MM-DD').
    end_date (str): The ending date of the period to be removed (format 'YYYY-MM-DD').
    col (ee.ImageCollection): The image collection to be filtered.

    Returns:
    ee.ImageCollection: The new collection that does not contain the removed period.
    """
    bad_data_filter = ee.Filter.date(start_date, end_date)
    print(f"Period from {start_date} to {end_date} removed")
    return col.filter(bad_data_filter.Not())


def stats(image, aoi, scale):
    """
    Calculate mean and standard deviation for each band in an image.

    Parameters:
    image (ee.Image): The image to be analyzed.
    aoi (ee.Geometry): The area of interest for the statistics.
    scale (int): The scale in meters for the analysis.

    Returns:
    dict: A dictionary containing the mean and standard deviation for each band.
    """
    return image.reduceRegion(
        reducer=ee.Reducer.mean().combine(
            reducer2=ee.Reducer.stdDev(),
            sharedInputs=True
        ),
        geometry=aoi,
        scale=scale,
        bestEffort=True  # Use maxPixels if you care about scale.
    )


def reduce_salt(image, aoi):
    """
    Sum the pixel values of the image within the specified area of interest.

    Parameters:
    image (ee.Image): The image to be analyzed.
    aoi (ee.Geometry): The area of interest for the reduction.

    Returns:
    ee.Feature: A feature containing the sum of pixel values.
    """
    reduced = image.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=aoi,
        scale=30
    )
    return ee.Feature(None, reduced)
