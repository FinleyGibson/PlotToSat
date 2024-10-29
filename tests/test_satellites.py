from datetime import date
from plottosat import config
from plottosat.satellites import *


class TestSentinelOne:

    def setup_class(cls):
        cls.satellite = SentinelOne()  

    def test_instantiation(self):
        assert isinstance(self.satellite, SentinelOne)

    def test_date_acquisition(self):
        start_date, end_date = self.satellite.get_start_finish_dates(2020)
        assert start_date == date(2020, 1, 1)
        assert end_date == date(2020, 12, 31)


class TestSentinelTwo:

    def setup_class(cls):
        cls.satellite = SentinelTwo()  

    def test_instantiation(self):
        assert isinstance(self.satellite, SentinelTwo)

    def test_date_acquisition(self):
        start_date, end_date = self.satellite.get_start_finish_dates(2020)
        assert start_date == date(2020, 1, 1)
        assert end_date == date(2020, 12, 31)

