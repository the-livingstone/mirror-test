from datetime import datetime
from pydantic import BaseModel

class WalkerSchema(BaseModel):
    name: str

class OrderSchema(BaseModel):
    walker: WalkerSchema
    apt_number: str
    pet_name: str
    pet_breed: str | None = None
    start_time: datetime
    duration: int

class DayOrdersSchema(BaseModel):
    orders: list[OrderSchema]

class PlaceOrderSchema(BaseModel):
    apt_number: str
    pet_name: str
    pet_breed: str | None = None
    start_time: datetime
    duration: int