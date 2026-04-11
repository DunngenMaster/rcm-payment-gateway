from app.core.constants import DEFAULT_LINE_ITEM_QUANTITY


class LineItemPayload:
    def __init__(self, name: str, price: int, quantity: int = DEFAULT_LINE_ITEM_QUANTITY):
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }
