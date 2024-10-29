from plottosat import config
from plottosat.satellites import *

def test_sentinel_one():
    satellite = SentinelOne()  
    assert isinstance(satellite, SentinelOne)

def test_sentinel_two():
    satellite = SentinelTwo()  
    assert isinstance(satellite, SentinelTwo)
    assert isinstance(satellite.all_bands, list)