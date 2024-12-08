import pytest

from datetime import date
from plottosat.sentinel_one import SentinelOne
from plottosat.sentinel_two import SentinelTwo
from ee.imagecollection import ImageCollection
import ee


class TestSentinelOne:
    def setup_class(cls):
        ee.Authenticate()
        ee.Initialize(project="plottosat-fjgibson")
        cls.satellite = SentinelOne()

    def test_instantiation(self):
        assert isinstance(self.satellite, SentinelOne)

    def test_date_acquisition(self):
        start_date, end_date = self.satellite.get_year_start_finish_dates(2020)
        assert start_date == date(2020, 1, 1)
        assert end_date == date(2020, 12, 31)

        with pytest.raises(ValueError):
            start_date, end_date = self.satellite.get_year_start_finish_dates(2013)

    def test_generate_base_cllection(self):
        geometry = ee.Geometry.Polygon(
            [
                [
                    [-2.97404756802236, 41.99472813320794],
                    [-2.97404756802236, 41.8107480842418],
                    [-2.66643038052236, 41.8107480842418],
                    [-2.66643038052236, 41.99472813320794],
                ]
            ]
        )

        out = self.satellite._generate_base_collection(
            start_date=date(2020, 1, 1), end_date=date(2020, 1, 2), geometry=geometry
        )

        assert isinstance(out, ImageCollection)


class TestSentinelTwo:
    def setup_class(cls):
        cls.satellite = SentinelTwo()

    def test_instantiation(self):
        assert isinstance(self.satellite, SentinelTwo)

    def test_date_acquisition(self):
        start_date, end_date = self.satellite.get_start_finish_dates(2020)
        assert start_date == date(2020, 1, 1)
        assert end_date == date(2020, 12, 31)

        with pytest.raises(ValueError):
            start_date, end_date = self.satellite.get_start_finish_dates(2014)
