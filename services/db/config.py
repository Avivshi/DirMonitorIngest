def get_connection_details() -> dict:
    """
    Returns the database connection details.

    :return: A dictionary containing the connection details for the database.
    """
    return {
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5433",
        "database": "postgres_db",
    }

