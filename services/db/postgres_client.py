from sqlalchemy import create_engine, Column
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database, drop_database

from models import Base


class PostgresDB:
    def __init__(self, connection_details: dict):
        """
        Initialize the PostgresDB instance with the provided connection details.

        :param connection_details: A dictionary containing connection details for the database.
        """
        connection_string = _generate_connection_string(connection_details=connection_details)
        try:
            self._engine = create_engine(connection_string)
            session_factory = sessionmaker(bind=self._engine)
            self._session = scoped_session(session_factory=session_factory)
        except SQLAlchemyError as e:
            raise e

    def __enter__(self):
        """
        Enter the context of the PostgresDB instance.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context of the PostgresDB instance, closing the connection.
        """
        self.close()

    def initialize(self):
        """
        Create all tables defined in the SQLAlchemy models if they do not exist.
        """
        try:
            Base.metadata.create_all(bind=self._engine)
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Error initializing the database: {e}") from e

    def insert(self, model: Base, data: list[dict]):
        """
        Insert data into the specified model's table.

        :param model: The SQLAlchemy model to insert data into.
        :param data: A list of dictionaries representing the data to be inserted.
        """
        try:
            model.insert_data(self, data)
        except SQLAlchemyError as e:
            self.session.rollback()
            raise SQLAlchemyError(f"Error inserting data: {e}") from e

    def execute(self, query):
        """
        Execute a SQL query.

        :param query: The SQL query to execute
        :return: The result of the query
        """
        try:
            result = self.session.execute(query)
            self.session.commit()
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            raise SQLAlchemyError(f"Error executing query: {e}") from e

    def select(self, model: Base, columns: list = None, distinct_column: Column = None, **kwargs):
        """
        Select records from the specified model's table.

        :param model: The SQLAlchemy model to select records from.
        :param columns: List of columns to retrieve.
        :param distinct_column: Optional distinct column for selecting distinct values.
        :param kwargs: Optional keyword arguments for filtering records.
        :return: A list of selected records or distinct values.
        """
        query = self.session.query(*[getattr(model, col) for col in columns]) if columns else self.session.query(model)

        if distinct_column:
            query = query.distinct(distinct_column)

        if kwargs:
            query = query.filter_by(**kwargs)

        return query.all()

    @property
    def session(self):
        """
        Returns the SQLAlchemy session.
        """
        return self._session()

    def close(self):
        """
        Close the database session and dispose of the engine.
        """
        self._session.close()
        self._engine.dispose()

    @classmethod
    def create_database(cls, config):
        """
        Create the database if it does not exist.

        :param config: The database connection details.
        """
        connection_string = _generate_connection_string(config)
        if not database_exists(connection_string):
            create_database(connection_string)

    @classmethod
    def drop_database(cls, config):
        """
        Drop the database if it exists.

        :param config: The database connection details.
        """
        connection_string = _generate_connection_string(config)
        if database_exists(connection_string):
            drop_database(connection_string)


def _generate_connection_string(connection_details: dict) -> str:
    """
    Generate the connection string for the PostgreSQL database.

    :param connection_details: Dictionary containing connection details
    :return: The connection string
    """
    user = connection_details.get("user")
    password = connection_details.get("password")
    host = connection_details.get("host")
    port = connection_details.get("port")
    database = connection_details.get("database")

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"
