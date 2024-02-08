from datetime import datetime

from pydantic import BaseModel, Field, NaiveDatetime


def nearest_time():
    t = datetime.now()
    return t.replace(
        second=0,
        microsecond=0,
        minute=0 if t.minute >= 30 else 30,
        hour=t.hour + 1 if t.minute >= 30 else t.hour,
    )


class WalkerSchema(BaseModel):
    name: str


class OrderSchema(BaseModel):
    walker: WalkerSchema
    apt_number: str
    pet_name: str
    pet_breed: str | None = None
    start_time: NaiveDatetime
    duration: int


class DayOrdersSchema(BaseModel):
    orders: list[OrderSchema]


class PlaceOrderSchema(BaseModel):
    apt_number: str
    pet_name: str
    pet_breed: str | None = None
    start_time: NaiveDatetime = Field(default_factory=nearest_time)
    duration: int = Field(default=10)
