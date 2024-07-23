from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import insert
from services.db.postgres_client import PostgresDB
from models import Base


class ObjectsDetectionEvent(Base):
    __tablename__ = 'objects_detection_events'

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String, index=True)
    detection_time = Column(TIMESTAMP(timezone=True))
    detections = Column(JSON)

    @staticmethod
    def insert_data(db: PostgresDB, data: list[dict]):
        """
        Insert data into the objects_detection_events table.

        :param db: Instance of PostgresDB to handle database operations.
        :param data: A list of dictionaries representing the data to be inserted.
        """
        query = ObjectsDetectionEvent.__table__.insert().values(data)
        db.execute(query)


class VehicleStatus(Base):
    """
    SQLAlchemy model for the vehicle_status table.

    Attributes:
        vehicle_id (str): Primary key of the table. The ID of the vehicle.
        report_time (TIMESTAMP): The timestamp when the status was reported.
        status (str): The current status of the vehicle (e.g., driving, parking).
    """
    __tablename__ = 'vehicle_status'

    vehicle_id = Column(String, primary_key=True, index=True)
    report_time = Column(TIMESTAMP(timezone=True))
    status = Column(String)

    @staticmethod
    def insert_data(db: PostgresDB, data: list[dict]):
        """
        Insert or update data into the vehicles_status table.

        :param db: Instance of PostgresDB to handle database operations.
        :param data: A list of dictionaries representing the data to be inserted or updated.
        """
        stmt = insert(VehicleStatus).values(data)
        update_dict = {c.name: c for c in stmt.excluded if c.name != 'vehicle_id'}
        on_conflict_stmt = stmt.on_conflict_do_update(
            index_elements=['vehicle_id'],
            set_=update_dict
        )
        db.execute(on_conflict_stmt)
