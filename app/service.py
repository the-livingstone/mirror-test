import pdb
import random
from sqlalchemy.orm import Session
from app.db.repo import OrdersRepo
from app.errors import RepresentativeError
from app.models import Order, Walker
from pydantic import ValidationError

from app.schemas import PlaceOrderSchema, WalkerSchema

class OrderServiceError(RepresentativeError):
    pass

class OrderService:

    def __init__(self, session: Session) -> None:
        self.repo = OrdersRepo(session)

    def place_order(self, params: PlaceOrderSchema):
        free_walkers = self.repo.get_free_walkers(params.start_time)
        if not free_walkers:
            raise OrderServiceError(title='No free walkers at the time')
        selected_walker = random.choice(free_walkers)
        dump = params.model_dump()
        dump.update({"walker": selected_walker.model_dump()})
        try:
            order = Order.model_validate(dump)
        except ValidationError as e:
            raise OrderServiceError(title=str(e.errors()))

        self.repo.place_order(order)
        self.repo.session.commit()
        return order
    
    def add_walker(self, params: WalkerSchema):
        walker = Walker.model_validate(params.model_dump())
        self.repo.add_walker(walker)
        self.repo.session.commit()
        return walker