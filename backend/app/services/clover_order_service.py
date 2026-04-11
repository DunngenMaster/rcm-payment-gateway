from app.clients.clover_client import clover_client

class CloverOrderService:
    async def create_order(self, title: str = "Demo Order", currency: str = "USD"):
        merchant_id = clover_client.get_merchant_id()
        endpoint = f"/v3/merchants/{merchant_id}/orders"

        payload = {
            "title": title,
            "currency": currency
        }
        print("ORDER ENDPOINT:", endpoint)
        return await clover_client.post(endpoint, payload)

    async def add_line_item(self, order_id: str, name: str, price: int, quantity: int = 1):
        merchant_id = clover_client.get_merchant_id()
        endpoint = f"/v3/merchants/{merchant_id}/orders/{order_id}/line_items"

        payload = {
            "name": name,
            "price": price,
            "quantity": quantity
        }
        return await clover_client.post(endpoint, payload)

    async def get_order(self, order_id: str):
        merchant_id = clover_client.get_merchant_id()
        endpoint = f"/v3/merchants/{merchant_id}/orders/{order_id}"
        return await clover_client.get(endpoint)

clover_order_service = CloverOrderService()