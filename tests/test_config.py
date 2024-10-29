import toml
from plottosat import DIR_ROOT

CONFIG_File = DIR_ROOT / "config.toml"

def test_file_exists():
    assert CONFIG_File.is_file()


config = toml.load(CONFIG_File)

def test_sentinel1():
    assert config["sentinel1_info"] != None