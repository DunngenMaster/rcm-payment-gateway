from pydantic import BaseModel
from app.core.constants import DEFAULT_CHARGE_CURRENCY, DEFAULT_CHARGE_DESCRIPTION


class CreateChargeRequest(BaseModel):
    amount: int
    source: str
    currency: str = DEFAULT_CHARGE_CURRENCY
    description: str = DEFAULT_CHARGE_DESCRIPTION
