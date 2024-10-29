from pathlib import Path
import toml
import logging
import os

DIR_ROOT = Path(__file__).parent.parent.parent
DIR_DATA = DIR_ROOT / "data"
DIR_LOGS = DIR_ROOT / "logs"


FILE_CONFIG = DIR_ROOT / "config.toml"
config = toml.load(FILE_CONFIG)

# Set up logging directory and file
os.makedirs(DIR_LOGS, exist_ok=True)
FILE_LOG = DIR_LOGS / "app.log"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the lowest level to capture (DEBUG will capture all levels)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler(FILE_LOG)  # Log to a file
    ]
)

# Create a custom logger
logger = logging.getLogger("app_logger")