from datetime import date
from fastapi import Depends, APIRouter
from app.db.repo import OrdersRepo
from app.deps import get_repo, get_service
from app.errors import RepresentativeError
from app.schemas import DayOrdersSchema, OrderSchema, PlaceOrderSchema, WalkerSchema
from app.service import OrderService

router = APIRouter()


@router.get("/orders/{day}", response_model=DayOrdersSchema)
async def get_day_orders(
    day: str,
    repo: OrdersRepo = Depends(get_repo)
):
    try:
        dt = date.fromisoformat(day)
    except ValueError:
        return RepresentativeError(title="wrong date format")
    orders = repo.get_day_orders(dt)
    return DayOrdersSchema(orders=[x.model_dump() for x in orders])

@router.post("/orders", response_model=OrderSchema)
async def place_order(
    intake: PlaceOrderSchema,
    service: OrderService = Depends(get_service)
):
    order = service.place_order(intake)
    return order

@router.post("/walker", response_model=WalkerSchema)
async def add_new_walker(
    intake: WalkerSchema,
    service: OrderService = Depends(get_service)
):
    walker = service.add_walker(intake)
    return walker