from datetime import datetime
from typing import Self
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint

from sqlalchemy.orm import Mapped, relationship
from app.db.base_db import Base
from app.models import Order, Walker



class WalkerORM(Base):
    __tablename__ = "walkers"

    uid: Mapped[str] = Column(String, primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)

    _unique_constraint = UniqueConstraint(name)

    def to_entity(self) -> Walker:
        return Walker(
            uid=self.uid,
            name=self.name,
        )
    
    @classmethod
    def from_entity(cls, walker: Walker) -> Self:
        return cls(
            uid=walker.uid,
            name=walker.name,
        )

class OrderORM(Base):
    __tablename__ = "orders"

    uid: Mapped[str] = Column(String, primary_key=True)
    walker_uid: Mapped[int] = Column(String, ForeignKey("walkers.uid"), nullable=False)
    apt_number: Mapped[str] = Column(String, nullable=False)
    pet_name: Mapped[str] = Column(String, nullable=False)
    pet_breed: Mapped[str] = Column(String)
    start_day: Mapped[str] = Column(String, nullable=False)
    start_time: Mapped[str] = Column(String, nullable=False)
    duration: Mapped[int] = Column(Integer, nullable=False)

    _unique_constraint = UniqueConstraint(walker_uid, start_day, start_time)
    walker: Mapped[WalkerORM] = relationship("WalkerORM")

    def to_entity(self) -> Order:
        return Order(
            uid=self.uid,
            walker=self.walker.to_entity(),
            apt_number=self.apt_number,
            pet_name=self.pet_name,
            pet_breed=self.pet_breed,
            start_time=datetime.fromisoformat(f"{self.start_day}T{self.start_time}"),
            duration=self.duration,
        )

    @classmethod
    def from_entity(cls, order: Order) -> Self:
        return cls(
            uid=order.uid,
            walker_uid=order.walker.uid,
            apt_number=order.apt_number,
            pet_name=order.pet_name,
            pet_breed=order.pet_breed,
            start_day=order.start_time.strftime("%F"),
            start_time=order.start_time.strftime("%T"),
            duration=order.duration,
        )