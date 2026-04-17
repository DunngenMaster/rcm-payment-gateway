from app.clients.clover_client import clover_client
from app.core.constants import DEFAULT_ORDER_TITLE, DEFAULT_ORDER_CURRENCY, DEFAULT_LINE_ITEM_QUANTITY
from app.models import OrderPayload, LineItemPayload


class CloverOrderService:
    async def create_order(self, title: str = DEFAULT_ORDER_TITLE, currency: str = DEFAULT_ORDER_CURRENCY, merchant_id: str = None):
        """Create order for a specific merchant"""
        m_id = clover_client.get_merchant_id(merchant_id)
        endpoint = f"/v3/merchants/{m_id}/orders"
        payload = OrderPayload(title, currency)
        return await clover_client.post(endpoint, payload.to_dict(), merchant_id)

    async def add_line_item(self, order_id: str, name: str, price: int, quantity: int = DEFAULT_LINE_ITEM_QUANTITY, merchant_id: str = None):
        """Add line item to order for a specific merchant"""
        m_id = clover_client.get_merchant_id(merchant_id)
        endpoint = f"/v3/merchants/{m_id}/orders/{order_id}/line_items"
        payload = LineItemPayload(name, price, quantity)
        return await clover_client.post(endpoint, payload.to_dict(), merchant_id)

    async def delete_line_item(self, order_id: str, line_item_id: str, merchant_id: str = None):
        """Delete line item from order for a specific merchant"""
        m_id = clover_client.get_merchant_id(merchant_id)
        endpoint = f"/v3/merchants/{m_id}/orders/{order_id}/line_items/{line_item_id}"
        return await clover_client.delete(endpoint, merchant_id)

clover_order_service = CloverOrderService()