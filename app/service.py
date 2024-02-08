import random

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.db.repo import OrdersRepo
from app.errors import RepresentativeError
from app.models import Order
from app.schemas import PlaceOrderSchema


class OrderServiceError(RepresentativeError):
    pass


class OrderService:

    def __init__(self, session: Session) -> None:
        self.repo = OrdersRepo(session)

    def _get_err_msg(self, ex: ValidationError):
        msg = "; ".join([x.get("msg", "") for x in ex.errors()])
        return msg

    def place_order(self, params: PlaceOrderSchema):
        free_walkers = self.repo.get_free_walkers(params.start_time)
        if not free_walkers:
            raise OrderServiceError(title="No free walkers at the time")
        selected_walker = random.choice(free_walkers)
        dump = params.model_dump()
        dump.update({"walker": selected_walker.model_dump()})
        try:
            order = Order.model_validate(dump)
        except ValidationError as e:
            raise OrderServiceError(title=self._get_err_msg(e))

        self.repo.place_order(order)
        self.repo.session.commit()
        return order
