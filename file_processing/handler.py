import os

from pydantic import ValidationError
from json.decoder import JSONDecodeError
from sqlalchemy.exc import SQLAlchemyError
from watchdog.events import FileSystemEventHandler

from services.db.postgres_client import PostgresDB
from file_processing.loader import load_objects_detection_events, load_vehicle_status
from logger_config import get_logger

OBJECT_NAME_PREFIX = "objects_detection"
VEHICLES_STATUS_PREFIX = "vehicle_status"

# Mapping of prefixes to corresponding load functions
LOAD_FUNCS = {
    OBJECT_NAME_PREFIX: load_objects_detection_events,
    VEHICLES_STATUS_PREFIX: load_vehicle_status,
}

# Set up logging
logger = get_logger(__name__)


def get_prefix(file_name: str) -> str | None:
    """
    Determine the prefix of the file name to identify its type.

    :param file_name: Name of the file to check.
    :return: The prefix string if it matches known prefixes, else None.
    """
    for prefix in LOAD_FUNCS:
        if file_name.startswith(prefix):
            return prefix
    return


def load_file(file_name: str, file_path: str, db: PostgresDB):
    """
    Load data from the file into the database based on the file prefix.

    :param file_name: Name of the file to check.
    :param file_path: Path to the file to be loaded.
    :param db: Instance of PostgresDB to handle database operations.
    """
    prefix = get_prefix(file_name=file_name)
    load_func = LOAD_FUNCS.get(prefix)
    if not load_func:
        logger.warning(f"No load function found for file name: {file_name}")
        return
    try:
        load_func(file_path=file_path, db=db)
        logger.info(f"Successfully loaded file: {file_path}")
    except JSONDecodeError as e:
        logger.error(f"JSON decode error for file {file_path}: {e}")
    except ValidationError as e:
        logger.error(f"Validation error for file {file_path}: {e}")
    except SQLAlchemyError as e:
        logger.error(f"Database error for file {file_path}: {e}")


class NewFileHandler(FileSystemEventHandler):
    """
    Event handler for monitoring new file creation in the directory.
    """

    def __init__(self, db: PostgresDB):
        self.db = db

    def on_created(self, event):
        """
        Handle the event when a new file is created.

        :param event: The event representing the file creation.
        """
        if event.is_directory:
            return  # Ignore directory creation events

        file_path = event.src_path
        logger.info(f"Detected new file: {file_path}")
        file_name = os.path.basename(file_path)
        load_file(file_name=file_name, file_path=file_path, db=self.db)
