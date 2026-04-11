from app.models import CodeExchangeRequest
from app.services.clover_oauth_service import clover_oauth_service
from app.clients.clover_client import clover_client
from app.db.token_store import token_store
from app.core.constants import (
    RESPONSE_KEY_SUCCESS,
    RESPONSE_KEY_MESSAGE,
    RESPONSE_KEY_TOKEN_DATA,
    MSG_AUTH_CONNECTED,
    OAUTH_PARAM_MERCHANT_ID,
)


class AuthHandler:

    async def start_auth(self) -> str:
        return clover_oauth_service.get_authorize_url()

    async def exchange_code(self, payload: CodeExchangeRequest) -> dict:
        token_data = await clover_oauth_service.exchange_code_for_token(
            payload.code,
            payload.merchant_id
        )
        # Save merchant_id along with token data
        token_data[OAUTH_PARAM_MERCHANT_ID] = payload.merchant_id
        token_store.save_token(token_data)
        
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_MESSAGE: MSG_AUTH_CONNECTED,
            RESPONSE_KEY_TOKEN_DATA: token_data
        }

    async def check_connection(self) -> dict:
        access_token = token_store.get_access_token()
        merchant_id = token_store.get_merchant_id()

        if not access_token or not merchant_id:
            return {
                "connected": False,
                "message": "Clover not connected"
            }

        try:
            endpoint = f"/v3/merchants/{merchant_id}"
            await clover_client.get(endpoint)
            return {
                "connected": True,
                "message": "Clover connected"
            }
        except Exception:
            return {
                "connected": False,
                "message": "Clover session expired"
            }
