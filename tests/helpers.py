import os
import json
import shutil
from datetime import datetime, timezone
from sqlalchemy import Row


# Determine the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Constants
TEST_DIRECTORY_TO_WATCH = os.path.join(BASE_DIR, 'test_input_data')
TEST_DATA_DIRECTORY = os.path.join(BASE_DIR, 'test_data')

OBJECTS_DETECTION_FILE_NAME = "objects_detection_20240721T143000.json"
VEHICLE_STATUS_FILE_NAME = "vehicle_status_20240721T143000.json"
OBJECTS_DETECTION_TABLE = "objects_detection_events"
VEHICLE_STATUS_TABLE = "vehicle_status"

TEST_DB_CONFIG = {
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5433",
    "database": "test_postgres_db",
}


def create_input_directory(directory_path: str = TEST_DIRECTORY_TO_WATCH):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def delete_input_directory(directory_path: str = TEST_DIRECTORY_TO_WATCH):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)


def adjust_result_format(result: list[Row], table: str):
    tables_mapping = {OBJECTS_DETECTION_TABLE: _map_object_detection, VEHICLE_STATUS_TABLE: _map_vehicle_status}
    return [tables_mapping[table](row) for row in result]


def read_json_file(file_name: str) -> dict:
    with open(os.path.join(TEST_DATA_DIRECTORY, file_name), 'r') as test_file:
        return json.load(test_file)


def copy_test_data(file_name: str):
    src_path = os.path.join(TEST_DATA_DIRECTORY, file_name)
    dst_path = os.path.join(TEST_DIRECTORY_TO_WATCH, file_name)
    shutil.copy(src_path, dst_path)


def parse_datetime(datetime_str: str) -> datetime:
    return datetime.fromisoformat(datetime_str).astimezone(timezone.utc)


def _map_object_detection(row: Row) -> dict:
    return {
        'vehicle_id': row.vehicle_id,
        'detection_time': row.detection_time,
        'detections': row.detections
    }


def _map_vehicle_status(row: Row) -> dict:
    return {
        'vehicle_id': row.vehicle_id,
        'report_time': row.report_time,
        'status': row.status
    }
