from plottosat.maps import Map
import folium


def test_instantiation():
    map = Map(location=(0, 0), zoom_start=10)
    assert isinstance(map, folium.Map)


def test_add_ee_layer():
    map = Map(location=(0, 0), zoom_start=10)
    assert hasattr(map, "add_ee_layer")
