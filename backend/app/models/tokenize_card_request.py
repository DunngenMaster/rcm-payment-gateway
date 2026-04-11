from pydantic import BaseModel


class TokenizeCardRequest(BaseModel):
    ecommerce_key: str
    number: str
    exp_month: int
    exp_year: int
    cvc: str
    zip: str
