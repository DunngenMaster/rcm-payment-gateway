from app.clients.clover_client import clover_client
import time

class CloverPaymentService:
    async def create_payment(self, order_id: str, amount: int, tip_amount: int = 0):
        merchant_id = clover_client.get_merchant_id()
        endpoint = f"/v3/merchants/{merchant_id}/orders/{order_id}/payments"

        payload = {
            "amount": amount,
            "tipAmount": tip_amount
        }
        return await clover_client.post(endpoint, payload)

    async def create_demo_payment(self, order_id: str, amount: int, tip_amount: int = 0):
        """Demo payment that simulates successful payment processing"""
        # In a real app, this would integrate with Clover's payment processing
        # For demo purposes, we'll simulate a successful payment

        payment_id = f"demo_{order_id}_{int(time.time())}"

        demo_payment = {
            "id": payment_id,
            "order": {"id": order_id},
            "amount": amount,
            "tipAmount": tip_amount,
            "taxAmount": 0,
            "result": "SUCCESS",
            "createdTime": int(time.time() * 1000),
            "modifiedTime": int(time.time() * 1000),
            "tender": {
                "label": "Demo Card",
                "labelKey": "com.clover.tender.demo"
            }
        }

        return demo_payment

    async def get_payment(self, order_id: str, payment_id: str):
        merchant_id = clover_client.get_merchant_id()
        endpoint = f"/v3/merchants/{merchant_id}/orders/{order_id}/payments/{payment_id}"
        return await clover_client.get(endpoint)

    async def get_order_payments(self, order_id: str):
        merchant_id = clover_client.get_merchant_id()
        endpoint = f"/v3/merchants/{merchant_id}/orders/{order_id}/payments"
        return await clover_client.get(endpoint)

clover_payment_service = CloverPaymentService()