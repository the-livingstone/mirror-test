from datetime import datetime

from pydantic import BaseModel, Field, NaiveDatetime, field_validator
from xid import XID


def get_uid():
    return XID().string()


class Walker(BaseModel):
    uid: str = Field(default_factory=get_uid)
    name: str


class Order(BaseModel):
    uid: str = Field(default_factory=get_uid)
    walker: Walker
    apt_number: str
    pet_name: str
    pet_breed: str | None
    start_time: NaiveDatetime
    duration: int

    @field_validator("duration")
    @classmethod
    def check_duration(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Walk duration should be greater than 0")
        elif value > 30:
            raise ValueError("Walk duration should not exceed 30 minutes")
        return value

    @field_validator("start_time")
    @classmethod
    def check_start_time(cls, value: NaiveDatetime) -> NaiveDatetime:
        if value < datetime.now():
            raise ValueError("Please, do not book walks in the past")
        if value.hour < 7 or (value.hour >= 23 and value.minute > 0):
            raise ValueError("The walk should be booked between 7:00 and 23:00")
        if value.minute % 30:
            raise ValueError("Please, select strait 30 min interval for booking")
        return value
