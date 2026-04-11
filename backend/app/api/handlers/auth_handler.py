from app.models import CodeExchangeRequest
from app.services.clover_oauth_service import clover_oauth_service
from app.core.constants import (
    RESPONSE_KEY_SUCCESS,
    RESPONSE_KEY_MESSAGE,
    RESPONSE_KEY_TOKEN_DATA,
    MSG_AUTH_CONNECTED,
)


class AuthHandler:

    async def start_auth(self) -> str:
        return clover_oauth_service.get_authorize_url()

    async def exchange_code(self, payload: CodeExchangeRequest) -> dict:
        token_data = await clover_oauth_service.exchange_code_for_token(
            payload.code,
            payload.merchant_id
        )
        return {
            RESPONSE_KEY_SUCCESS: True,
            RESPONSE_KEY_MESSAGE: MSG_AUTH_CONNECTED,
            RESPONSE_KEY_TOKEN_DATA: token_data
        }
