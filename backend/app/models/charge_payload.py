from app.core.constants import DEFAULT_CHARGE_CURRENCY, DEFAULT_CHARGE_DESCRIPTION, CLOVER_ECOMIND_ECOM


class ChargePayload:
    def __init__(self, amount: int, source: str, currency: str = DEFAULT_CHARGE_CURRENCY, 
                 description: str = DEFAULT_CHARGE_DESCRIPTION):
        self.amount = amount
        self.source = source
        self.currency = currency
        self.description = description

    def to_dict(self) -> dict:
        return {
            "amount": self.amount,
            "currency": self.currency.lower(),
            "source": self.source,
            "description": self.description,
            "ecomind": CLOVER_ECOMIND_ECOM
        }
