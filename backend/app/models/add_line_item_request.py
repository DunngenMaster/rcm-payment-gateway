from pydantic import BaseModel
from app.core.constants import DEFAULT_LINE_ITEM_QUANTITY


class AddLineItemRequest(BaseModel):
    order_id: str
    name: str
    price: int
    quantity: int = DEFAULT_LINE_ITEM_QUANTITY
