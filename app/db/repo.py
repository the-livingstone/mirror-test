from datetime import date, datetime

from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.orm import OrderORM, WalkerORM
from app.errors import RepresentativeError
from app.models import Order, Walker


class OrdersRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_day_orders(self, day: date) -> list[Order]:
        items = (
            self.session.query(OrderORM)
            .where(OrderORM.start_day == day.isoformat())
            .order_by(OrderORM.start_time)
            .all()
        )
        return [x.to_entity() for x in items]

    def place_order(self, order: Order):
        try:
            self.session.add(OrderORM.from_entity(order))
            self.session.flush()
            return order
        except IntegrityError as e:
            raise RepresentativeError(title=e)

    def get_free_walkers(self, start_time: datetime) -> list[Walker]:
        orders_at_time = select(OrderORM.walker_uid).where(
            and_(
                OrderORM.start_day == start_time.strftime("%F"),
                OrderORM.start_time == start_time.strftime("%T"),
            )
        )
        free_walkers = self.session.query(WalkerORM).where(
            WalkerORM.uid.not_in(orders_at_time)
        )
        return [x.to_entity() for x in free_walkers]

    def add_walker(self, walker: Walker):
        try:
            self.session.add(WalkerORM.from_entity(walker))
            self.session.flush()
            return walker
        except IntegrityError as e:
            raise RepresentativeError(title=e)
