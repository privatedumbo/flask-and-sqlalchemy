from src.core.errors import UnableToMapRecordError, UndefinedValueInRecord

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Temperature(Base):
    """Temperature model. Defined based on input file."""

    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, nullable=False)
    timestamp = Column(DateTime)
    temperature = Column(Float)
    duration = Column(String(128))

    def __init__(self, id: int, timestamp: str, temperature: float, duration: str):
        self.id = id
        self.timestamp = timestamp
        self.temperature = temperature
        self.duration = duration

    @staticmethod
    def dict_from_tuple(record: tuple) -> dict:
        """
        Based on a row from the file, maps it to a dict to later use it on Temperature instantiation.
        Args:
            record (tuple): row from the file as a tuple.
        Returns:
            dict: dict where each key is a Temperature attribute.
        Raises:
            `src.core.errors.UnableToMapRecordError`: when the dict with Temperature attributes cannot be created
                either due to the input data type or to a missing attribute.
        """
        mapped_record = {}

        try:
            if not all(record) or len(record) > 4:
                raise UndefinedValueInRecord
            mapped_record = {
                "id": int(record[0]),
                "timestamp": record[1],
                "temperature": float(record[2]),
                "duration": record[3],
            }
        except (ValueError, IndexError, UndefinedValueInRecord) as e:
            raise UnableToMapRecordError("Unable to map {} - msg: {}".format(record, e))

        return mapped_record
