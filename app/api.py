from datetime import date

from fastapi import APIRouter, Depends

from app.db.repo import OrdersRepo
from app.deps import get_repo, get_service
from app.errors import RepresentativeError
from app.schemas import DayOrdersSchema, OrderSchema, PlaceOrderSchema
from app.service import OrderService

router = APIRouter()


@router.get("/orders/{day}", response_model=DayOrdersSchema)
async def get_day_orders(day: str, repo: OrdersRepo = Depends(get_repo)):
    """Вывести список заказов за день. Формат: YYYY-MM-DD"""
    try:
        dt = date.fromisoformat(day)
    except ValueError:
        return RepresentativeError(title="wrong date format")
    orders = repo.get_day_orders(dt)
    return DayOrdersSchema(orders=[x.model_dump() for x in orders])


@router.post("/orders", response_model=OrderSchema)
async def place_order(
    intake: PlaceOrderSchema, service: OrderService = Depends(get_service)
):
    """Разместить заказ
    Формат даты заказа: YYYY-MM-DDTHH:MM,</br>
    длительность прогулки указывается в минутах.</br>
    Прогулку можно забронировать с 7:00 до 23:00 каждый день, если есть свободные выгульщики.</br>
    Прогулка начинается в 00 или 30 минут каждого часа, и длится не более 30 минут.
    """
    order = service.place_order(intake)
    return order
