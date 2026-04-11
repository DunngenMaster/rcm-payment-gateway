from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.clover_order_service import clover_order_service
from app.services.clover_payment_service import clover_payment_service
from app.db.transaction_store import transaction_store

router = APIRouter(prefix="/payment", tags=["payment"])

class CreateOrderRequest(BaseModel):
    title: str = "Demo Order"
    currency: str = "USD"

class AddLineItemRequest(BaseModel):
    order_id: str
    name: str
    price: int
    quantity: int = 1

class CreatePaymentRequest(BaseModel):
    order_id: str
    amount: int
    tip_amount: int = 0

@router.post("/order")
async def create_order(payload: CreateOrderRequest):
    try:
        order = await clover_order_service.create_order(payload.title, payload.currency)

        # Log transaction
        transaction_store.log_transaction("order_created", {
            "order_id": order.get("id"),
            "title": payload.title,
            "currency": payload.currency
        })

        return {
            "success": True,
            "message": "Order created successfully",
            "order": order
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/line-item")
async def add_line_item(payload: AddLineItemRequest):
    try:
        line_item = await clover_order_service.add_line_item(
            payload.order_id, payload.name, payload.price, payload.quantity
        )

        # Log transaction
        transaction_store.log_transaction("line_item_added", {
            "order_id": payload.order_id,
            "line_item_id": line_item.get("id"),
            "name": payload.name,
            "price": payload.price,
            "quantity": payload.quantity
        })

        return {
            "success": True,
            "message": "Line item added successfully",
            "line_item": line_item
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pay")
async def create_payment(payload: CreatePaymentRequest):
    try:
        # Use demo payment for recruiter demo (no real card processing)
        payment = await clover_payment_service.create_demo_payment(
            payload.order_id, payload.amount, payload.tip_amount
        )

        # Log transaction
        transaction_store.log_transaction("payment_processed", {
            "order_id": payload.order_id,
            "payment_id": payment.get("id"),
            "amount": payload.amount,
            "tip_amount": payload.tip_amount,
            "result": payment.get("result")
        })

        return {
            "success": True,
            "message": "Demo payment processed successfully",
            "payment": payment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/order/{order_id}")
async def get_order(order_id: str):
    try:
        order = await clover_order_service.get_order(order_id)
        return {
            "success": True,
            "order": order
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/order/{order_id}/payments")
async def get_order_payments(order_id: str):
    try:
        payments = await clover_payment_service.get_order_payments(order_id)
        return {
            "success": True,
            "payments": payments
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions")
async def get_transactions():
    """Get all logged transactions"""
    try:
        transactions = transaction_store.get_all_transactions()
        return {
            "success": True,
            "transactions": transactions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))