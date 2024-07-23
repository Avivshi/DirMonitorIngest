# Directory Monitoring and Data Ingestion Application

## Overview

This application monitors a specified directory for new JSON files and loads their contents into a PostgreSQL database. The files can contain either objects detection events or vehicle status data. When a new file is added to the directory, the application processes it and inserts the validated data into the appropriate database tables.

## Project Structure

- `main.py`: Starts the directory monitoring process.
- `services/`: Contains the following subdirectories:
  - `db/`: Manages PostgreSQL database connection and operations.
    - `__init__.py`: Initializes the db module.
    - `config.py`: Provides database connection details.
    - `postgres_client.py`: Manages PostgreSQL database connection and operations.
  - `observer/`: Handles directory observation.
    - `__init__.py`: Initializes the observer module.
    - `observer_client.py`: Contains the DirectoryObserver class for monitoring the directory.
- `models/`: Contains the database and Pydantic models.
  - `__init__.py`: Initializes the models module.
  - `db_models.py`: SQLAlchemy models for the database tables.
  - `source_models.py`: Pydantic models for validating incoming JSON data.
- `file_processing/`: Manages file processing and data loading.
  - `__init__.py`: Initializes the file_processing module.
  - `handler.py`: Handles new file creation events and triggers data loading.
  - `loader.py`: Contains functions to load data from JSON files into the database.
- `logger_config.py`: Configures logging for the application.
- `tests/`: Contains the test cases and test data.
  - `helpers.py`: Helper functions for tests.
  - `test_integration.py`: Integration tests.
  - `test_data/`: Directory containing test JSON files.
- `sample_files/`: Directory containing sample JSON files for testing.
- `input/`: Directory to monitor for new JSON files.
- `requirements.txt`: Lists the necessary Python packages.
- `docker-compose.yaml`: Docker Compose configuration to set up the PostgreSQL database.

## Prerequisites

- Docker
- Python 3.11+
- PostgreSQL database

## Setup Instructions

1. **Install Python dependencies:**

   ```
   pip install -r requirements.txt
   ```

2. **Start the PostgreSQL database using Docker Compose:**

   ```
   docker compose up -d
   ```

   **Note:** You can connect to the PostgreSQL database using `psql` with the following command:
   
   ```
   psql -h localhost -p 5433 -U postgres -d postgres_db
   ```

3. **Run the application:**

   ```
   python main.py
   ```

The application will start monitoring the `input/` directory for new files. When a new JSON file is added, it will be processed and the data will be inserted into the database.

## Assumptions

- **Upsert for Vehicle Table:**
  It is assumed that we want to perform an upsert operation (insert or update) for the `vehicles_status` table when new records are added. This ensures that existing vehicle records are updated with the latest status, while new vehicle records are inserted.

## Sample Data

Sample JSON files for objects detection events and vehicle status are provided in the `sample_files/` directory. Use these files to test the application by copying them to the `input/` directory.

## Logging

The application logs its activity to both the console and a file named `app.log`. The logging configuration can be adjusted in `logger_config.py`.

## Integration Tests

Integration tests have been added to ensure the system works as expected.

   ```
   pytest tests/test_integration.py
   ```

These tests:

1. Create a test database.
2. Set up necessary directories.
3. Monitor a test directory for new files.
4. Simulate file creation and validate the data insertion into the database.
5. Clean up the test environment.

## Future Improvements

Given more time to invest, the following improvements would be implemented:

1. **Asynchronous Operation:**
   The task is I/O bound, so making it run asynchronously would improve performance and efficiency.

2. **Edge Cases and Unit Tests:**
   Adding more edge cases and unit tests to ensure the reliability and correctness of the code.

3. **Environment Variables:**
   Adding a `.env` file to manage configuration variables such as database details more securely and flexibly.