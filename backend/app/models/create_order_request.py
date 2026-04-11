from pydantic import BaseModel
from app.core.constants import DEFAULT_ORDER_TITLE, DEFAULT_ORDER_CURRENCY


class CreateOrderRequest(BaseModel):
    title: str = DEFAULT_ORDER_TITLE
    currency: str = DEFAULT_ORDER_CURRENCY
