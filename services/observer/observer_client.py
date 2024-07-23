from watchdog.observers import Observer
from services.db.postgres_client import PostgresDB
from file_processing.handler import NewFileHandler
from logger_config import get_logger


# Set up logging
logger = get_logger(__name__)


class DirectoryObserver(Observer):
    def __init__(self, directory_path: str, db: PostgresDB):
        super().__init__()
        self.directory_path = directory_path
        self.db = db

    def start_observer(self):
        """
        Start the observer to monitor the specified directory for new files.
        """
        event_handler = NewFileHandler(db=self.db)
        self.schedule(event_handler, self.directory_path, recursive=False)
        self.start()
        logger.info(f"Started monitoring directory: {self.directory_path}")

    def stop_observer(self):
        """
        Stop the observer.
        """
        self.stop()
        logger.info("Observer stopped by user.")
        self.join()
        logger.info("Observer thread has finished.")
