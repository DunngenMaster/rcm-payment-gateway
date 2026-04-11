from app.core.constants import DEFAULT_ORDER_TITLE, DEFAULT_ORDER_CURRENCY


class OrderPayload:
    def __init__(self, title: str = DEFAULT_ORDER_TITLE, currency: str = DEFAULT_ORDER_CURRENCY):
        self.title = title
        self.currency = currency

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "currency": self.currency
        }
