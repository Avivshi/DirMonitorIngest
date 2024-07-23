import time
import pytest
from models import Base
from services.db.postgres_client import PostgresDB
from main import DirectoryObserver
from tests.helpers import (
    read_json_file, VEHICLE_STATUS_FILE_NAME, OBJECTS_DETECTION_FILE_NAME,
    create_input_directory,
    delete_input_directory, OBJECTS_DETECTION_TABLE, VEHICLE_STATUS_TABLE, copy_test_data,
    adjust_result_format,
    parse_datetime, TEST_DIRECTORY_TO_WATCH, TEST_DB_CONFIG
)

# Read expected data
expected_objects_detection_data = read_json_file(OBJECTS_DETECTION_FILE_NAME)[OBJECTS_DETECTION_TABLE]
expected_vehicles_status_data = read_json_file(VEHICLE_STATUS_FILE_NAME)[VEHICLE_STATUS_TABLE]


# Fixtures
@pytest.fixture(scope='module')
def setup_test_environment():
    PostgresDB.create_database(config=TEST_DB_CONFIG)
    create_input_directory()
    yield TEST_DB_CONFIG
    PostgresDB.drop_database(config=TEST_DB_CONFIG)
    delete_input_directory()


@pytest.mark.parametrize("file_name,table,expected_data", [
    (OBJECTS_DETECTION_FILE_NAME, OBJECTS_DETECTION_TABLE, expected_objects_detection_data),
    (VEHICLE_STATUS_FILE_NAME, VEHICLE_STATUS_TABLE, expected_vehicles_status_data),
])
def test_file_insertion(setup_test_environment, file_name: str, table: str, expected_data: dict):
    db_config = setup_test_environment

    with PostgresDB(connection_details=db_config) as db:
        db.initialize()

        observer = DirectoryObserver(directory_path=TEST_DIRECTORY_TO_WATCH, db=db)
        observer.start_observer()

        copy_test_data(file_name=file_name)
        # Wait for the observer to detect the file and process it
        time.sleep(3)

        result = db.select(model=Base.metadata.tables[table])
        adjusted_result = adjust_result_format(result, table)

        for item in expected_data:
            if 'detection_time' in item:
                item['detection_time'] = parse_datetime(item['detection_time'])
            if 'report_time' in item:
                item['report_time'] = parse_datetime(item['report_time'])

        assert adjusted_result == expected_data

        observer.stop_observer()
