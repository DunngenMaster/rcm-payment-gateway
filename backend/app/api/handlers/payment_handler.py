import logging
from app.models import (
    CreateOrderRequest,
    AddLineItemRequest,
    TokenizeCardRequest,
    CreateChargeRequest,
)
from app.services.clover_order_service import clover_order_service
from app.services.clover_payment_service import clover_payment_service
from app.db.transaction_store import transaction_store, list_transactions
from app.clients.clover_client import clover_client
from app.core.constants import (
    CLOVER_TOKEN_SANDBOX_URL,
    CLOVER_TOKENS_ENDPOINT,
    CLOVER_CARD_KEY,
    CLOVER_CARD_NUMBER,
    CLOVER_CARD_EXP_MONTH,
    CLOVER_CARD_EXP_YEAR,
    CLOVER_CARD_CVV,
    CLOVER_CARD_ZIP,
    HEADER_API_KEY,
    HEADER_CONTENT_TYPE,
    HEADER_ACCEPT,
    CONTENT_TYPE_JSON,
    RESPONSE_KEY_SUCCESS,
    RESPONSE_KEY_MESSAGE,
    RESPONSE_KEY_ORDER,
    RESPONSE_KEY_LINE_ITEM,
    RESPONSE_KEY_KEY_DATA,
    RESPONSE_KEY_TOKEN_DATA,
    RESPONSE_KEY_PAYMENT,
    RESPONSE_KEY_TRANSACTIONS,
    TRANSACTION_LOG_TYPE_ORDER_CREATED,
    TRANSACTION_LOG_TYPE_LINE_ITEM_ADDED,
    TRANSACTION_LOG_KEY_ORDER_ID,
    TRANSACTION_LOG_KEY_TITLE,
    TRANSACTION_LOG_KEY_NAME,
    TRANSACTION_LOG_KEY_PRICE,
    MSG_ORDER_CREATED,
    MSG_ITEM_ADDED,
    MSG_ECOMMERCE_KEY_FETCHED,
    MSG_CARD_TOKENIZED,
    MSG_CHARGE_CREATED,
)
import httpx

logger = logging.getLogger(__name__)

class PaymentHandler:

    async def create_order(self, payload: CreateOrderRequest, merchant_id: str = None) -> dict:
        # Set merchant context in clover client
        if merchant_id:
            clover_client.set_merchant_id(merchant_id)
        
        order = await clover_order_service.create_order(payload.title, payload.currency, merchant_id)
        
        transaction_store.log_transaction(
            TRANSACTION_LOG_TYPE_ORDER_CREATED,
            {
                "merchant_id": merchant_id or clover_client.get_merchant_id(),
                TRANSACTION_LOG_KEY_ORDER_ID: order.get("id"),
                TRANSACTION_LOG_KEY_TITLE: payload.title
            },
            merchant_id
        )
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_MESSAGE: MSG_ORDER_CREATED,
            RESPONSE_KEY_ORDER: order
        }

    async def add_line_item(self, payload: AddLineItemRequest, merchant_id: str = None) -> dict:
        # Set merchant context
        if merchant_id:
            clover_client.set_merchant_id(merchant_id)
        
        line_item = await clover_order_service.add_line_item(
            payload.order_id, payload.name, payload.price, payload.quantity, merchant_id
        )
        
        transaction_store.log_transaction(
            TRANSACTION_LOG_TYPE_LINE_ITEM_ADDED,
            {
                "merchant_id": merchant_id or clover_client.get_merchant_id(),
                TRANSACTION_LOG_KEY_ORDER_ID: payload.order_id,
                TRANSACTION_LOG_KEY_NAME: payload.name,
                TRANSACTION_LOG_KEY_PRICE: payload.price
            },
            merchant_id
        )
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_MESSAGE: MSG_ITEM_ADDED,
            RESPONSE_KEY_LINE_ITEM: line_item
        }

    async def delete_line_item(self, order_id: str, line_item_id: str, merchant_id: str = None) -> dict:
        if merchant_id:
            clover_client.set_merchant_id(merchant_id)
        
        await clover_order_service.delete_line_item(order_id, line_item_id, merchant_id)
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_MESSAGE: "Line item deleted"
        }

    async def get_ecommerce_key(self, merchant_id: str = None) -> dict:
        if merchant_id:
            clover_client.set_merchant_id(merchant_id)
        
        key_data = await clover_payment_service.get_ecommerce_key(merchant_id)
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_MESSAGE: MSG_ECOMMERCE_KEY_FETCHED,
            RESPONSE_KEY_KEY_DATA: key_data
        }

    async def tokenize_card(self, payload: TokenizeCardRequest, merchant_id: str = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CLOVER_TOKEN_SANDBOX_URL}{CLOVER_TOKENS_ENDPOINT}",
                headers={
                    HEADER_API_KEY: payload.ecommerce_key,
                    HEADER_CONTENT_TYPE: CONTENT_TYPE_JSON,
                    HEADER_ACCEPT: CONTENT_TYPE_JSON
                },
                json={
                    CLOVER_CARD_KEY: {
                        CLOVER_CARD_NUMBER: payload.number,
                        CLOVER_CARD_EXP_MONTH: payload.exp_month,
                        CLOVER_CARD_EXP_YEAR: payload.exp_year,
                        CLOVER_CARD_CVV: payload.cvc,
                        CLOVER_CARD_ZIP: payload.zip
                    }
                }
            )
            response.raise_for_status()
            token_data = response.json()
            
            return {
                RESPONSE_KEY_SUCCESS: True,
                RESPONSE_KEY_MESSAGE: MSG_CARD_TOKENIZED,
                RESPONSE_KEY_TOKEN_DATA: token_data
            }

    async def create_charge(self, payload: CreateChargeRequest, merchant_id: str = None) -> dict:
        if merchant_id:
            clover_client.set_merchant_id(merchant_id)
        
        charge = await clover_payment_service.create_charge(
            payload.amount, payload.source, payload.currency, payload.description, merchant_id
        )
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_MESSAGE: MSG_CHARGE_CREATED,
            RESPONSE_KEY_PAYMENT: charge
        }

    def get_transactions(self, merchant_id: str = None) -> dict:
        transactions = list_transactions(merchant_id=merchant_id)
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_TRANSACTIONS: transactions
        }
