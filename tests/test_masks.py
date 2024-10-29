
import ee
from plottosat.masks import Masks
    
ee.Authenticate()
ee.Initialize(project='plottosat-fjgibson')

def test_one():
    countries = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
    geometry = countries.filter(ee.Filter.eq('country_na', 'Cyprus'))
    
    mask = Masks(geometry,{'aspectAsc':0})
    assert isinstance(mask, Masks)