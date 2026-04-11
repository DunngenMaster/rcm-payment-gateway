"""
Payment API Router - Routes payment endpoints to PaymentHandler.
"""

from fastapi import APIRouter, HTTPException

from app.models import (
    CreateOrderRequest,
    AddLineItemRequest,
    TokenizeCardRequest,
    CreateChargeRequest,
)
from app.api.handlers import PaymentHandler
from app.core.constants import (
    PAYMENT_ROUTER_PREFIX,
    PAYMENT_ROUTER_TAG,
    PAYMENT_ROUTE_ORDER,
    PAYMENT_ROUTE_LINE_ITEM,
    PAYMENT_ROUTE_ECOMMERCE_KEY,
    PAYMENT_ROUTE_TOKENIZE,
    PAYMENT_ROUTE_CHARGE,
    PAYMENT_ROUTE_TRANSACTIONS,
    HTTP_STATUS_INTERNAL_SERVER_ERROR,
    HTTP_STATUS_BAD_REQUEST,
)

# Initialize handler and router
payment_handler = PaymentHandler()
router = APIRouter(prefix=PAYMENT_ROUTER_PREFIX, tags=[PAYMENT_ROUTER_TAG])


@router.post(PAYMENT_ROUTE_ORDER)
async def create_order(payload: CreateOrderRequest):
    try:
        return await payment_handler.create_order(payload)
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"CREATE ORDER ERROR: {error_detail}")
        raise HTTPException(status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(PAYMENT_ROUTE_LINE_ITEM)
async def add_line_item(payload: AddLineItemRequest):
    try:
        return await payment_handler.add_line_item(payload)
    except Exception as e:
        raise HTTPException(status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(PAYMENT_ROUTE_LINE_ITEM)
async def delete_line_item(order_id: str, line_item_id: str):
    try:
        return await payment_handler.delete_line_item(order_id, line_item_id)
    except Exception as e:
        raise HTTPException(status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(PAYMENT_ROUTE_ECOMMERCE_KEY)
async def get_ecommerce_key():
    try:
        return await payment_handler.get_ecommerce_key()
    except Exception as e:
        raise HTTPException(status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(PAYMENT_ROUTE_TOKENIZE)
async def tokenize_card(payload: TokenizeCardRequest):
    try:
        return await payment_handler.tokenize_card(payload)
    except Exception as e:
        raise HTTPException(status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(PAYMENT_ROUTE_CHARGE)
async def create_charge(payload: CreateChargeRequest):
    try:
        return await payment_handler.create_charge(payload)
    except ValueError as e:
        error_msg = str(e)
        raise HTTPException(status_code=HTTP_STATUS_BAD_REQUEST, detail=error_msg)
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        raise HTTPException(status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR, detail=error_msg)


@router.get(PAYMENT_ROUTE_TRANSACTIONS)
async def get_transactions():
    try:
        return payment_handler.get_transactions()
    except Exception as e:
        raise HTTPException(status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR, detail=str(e))

