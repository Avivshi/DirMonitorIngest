import time

from services.db.config import get_connection_details
from services.db.postgres_client import PostgresDB
from services.observer.observer_client import DirectoryObserver

# Directory to monitor
DIRECTORY_TO_WATCH = 'input/'


def main():
    with PostgresDB(connection_details=get_connection_details()) as db:
        db.initialize()  # Initialize the database schema if needed
        observer = DirectoryObserver(directory_path=DIRECTORY_TO_WATCH, db=db)
    try:
        observer.start_observer()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop_observer()


if __name__ == "__main__":
    main()
