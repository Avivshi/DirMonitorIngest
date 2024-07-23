from pydantic import BaseModel
from datetime import datetime


class Detection(BaseModel):
    """
    Pydantic model for representing a detection event.

    Attributes:
        object_type (str): The type of object detected (e.g., car, pedestrian).
        object_value (int): The value associated with the detected object.
    """
    object_type: str
    object_value: int


class SourceObjectsDetectionEvent(BaseModel):
    """
    Pydantic model for representing an objects detection event.

    Attributes:
        vehicle_id (str): The ID of the vehicle that detected the objects.
        detection_time (datetime): The timestamp when the detection occurred.
        detections (List[Detection]): A list of Detection instances representing the detected objects.
    """
    vehicle_id: str
    detection_time: datetime
    detections: list[Detection]


class SourceVehicleStatus(BaseModel):
    """
    Pydantic model for representing the status of a vehicle.

    Attributes:
        vehicle_id (str): The ID of the vehicle.
        report_time (datetime): The timestamp when the status was reported.
        status (str): The current status of the vehicle (e.g., driving, parking).
    """
    vehicle_id: str
    report_time: datetime
    status: str
