from plottosat.satellites import *
from plottosat import config

def test_sentinel_one():
    satellite = SentinelOne(config["sentinel_one"])  