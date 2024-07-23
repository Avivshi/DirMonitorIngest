import json

from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import SQLAlchemyError

from services.db.postgres_client import PostgresDB
from models.db_models import ObjectsDetectionEvent, VehicleStatus, Base
from models.source_models import SourceObjectsDetectionEvent, SourceVehicleStatus


def load_objects_detection_events(file_path: str, db: PostgresDB):
    """
    Load objects detection events from a JSON file and insert them into the database.

    :param file_path: Path to the JSON file containing objects detection events.
    :param db: Instance of PostgresDB to handle database operations.
    :return: None
    """
    _load_data(
        file_path=file_path,
        db=db,
        source_model=SourceObjectsDetectionEvent,
        db_model=ObjectsDetectionEvent,
        data_key='objects_detection_events'
    )


def load_vehicle_status(file_path: str, db: PostgresDB):
    """
    Load vehicle status data from a JSON file and insert it into the database.

    :param file_path: Path to the JSON file containing vehicle status data.
    :param db: Instance of PostgresDB to handle database operations.
    :return: None
    """
    _load_data(
        file_path=file_path,
        db=db,
        source_model=SourceVehicleStatus,
        db_model=VehicleStatus,
        data_key='vehicle_status'
    )


def _load_data(
        file_path: str,
        db: PostgresDB,
        source_model: BaseModel,
        db_model: Base,
        data_key: str
):
    """
    General function to load data from a JSON file, validate it using a Pydantic model,
    and insert it into the database using a SQLAlchemy model.

    :param file_path: Path to the JSON file containing the data.
    :param db: Instance of PostgresDB to handle database operations.
    :param source_model: Pydantic model used for validating the data.
    :param db_model: SQLAlchemy model used for inserting the data into the database.
    :param data_key: Key in the JSON file where the relevant data is stored.
    """
    try:
        # Open and load data from the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Validate and transform data using the source model
        validated_data = [source_model(**item).model_dump() for item in data[data_key]]
        # Insert validated data into the database
        db.insert(model=db_model, data=validated_data)
    except json.decoder.JSONDecodeError as e:
        raise e
    except ValidationError as e:
        raise e
    except SQLAlchemyError as e:
        raise e
