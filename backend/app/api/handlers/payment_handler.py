from app.models import (
    CreateOrderRequest,
    AddLineItemRequest,
    TokenizeCardRequest,
    CreateChargeRequest,
)
from app.services.clover_order_service import clover_order_service
from app.services.clover_payment_service import clover_payment_service
from app.db.transaction_store import transaction_store, list_transactions
from app.core.constants import (
    CLOVER_TOKEN_SANDBOX_URL,
    CLOVER_TOKENS_ENDPOINT,
    CLOVER_CARD_KEY,
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


class PaymentHandler:

    async def create_order(self, payload: CreateOrderRequest) -> dict:
        order = await clover_order_service.create_order(payload.title, payload.currency)
        transaction_store.log_transaction(TRANSACTION_LOG_TYPE_ORDER_CREATED, {
            TRANSACTION_LOG_KEY_ORDER_ID: order.get("id"),
            TRANSACTION_LOG_KEY_TITLE: payload.title
        })
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_MESSAGE: MSG_ORDER_CREATED,
            RESPONSE_KEY_ORDER: order
        }

    async def add_line_item(self, payload: AddLineItemRequest) -> dict:
        line_item = await clover_order_service.add_line_item(
            payload.order_id, payload.name, payload.price, payload.quantity
        )
        transaction_store.log_transaction(TRANSACTION_LOG_TYPE_LINE_ITEM_ADDED, {
            TRANSACTION_LOG_KEY_ORDER_ID: payload.order_id,
            TRANSACTION_LOG_KEY_NAME: payload.name,
            TRANSACTION_LOG_KEY_PRICE: payload.price
        })
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_MESSAGE: MSG_ITEM_ADDED,
            RESPONSE_KEY_LINE_ITEM: line_item
        }

    async def delete_line_item(self, order_id: str, line_item_id: str) -> dict:
        await clover_order_service.delete_line_item(order_id, line_item_id)
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_MESSAGE: "Line item deleted"
        }

    async def get_ecommerce_key(self) -> dict:
        key_data = await clover_payment_service.get_ecommerce_key()
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_MESSAGE: MSG_ECOMMERCE_KEY_FETCHED,
            RESPONSE_KEY_KEY_DATA: key_data
        }

    async def tokenize_card(self, payload: TokenizeCardRequest) -> dict:
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
                        "number": payload.number,
                        "exp_month": payload.exp_month,
                        "exp_year": payload.exp_year,
                        "cvv": payload.cvc,
                        "zip": payload.zip
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

    async def create_charge(self, payload: CreateChargeRequest) -> dict:
        charge = await clover_payment_service.create_charge(
            payload.amount, payload.source, payload.currency, payload.description
        )
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_MESSAGE: MSG_CHARGE_CREATED,
            RESPONSE_KEY_PAYMENT: charge
        }

    def get_transactions(self) -> dict:
        transactions = list_transactions()
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_TRANSACTIONS: transactions
        }
