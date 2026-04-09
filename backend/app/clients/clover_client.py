from urllib.parse import urlencode
import httpx
from app.core.config import settings
from app.db.token_store import token_store
from app.core.constants import (
    OAUTH_AUTHORIZE_ENDPOINT,
    OAUTH_TOKEN_ENDPOINT,
    OAUTH_PARAM_CLIENT_ID,
    OAUTH_PARAM_RESPONSE_TYPE,
    OAUTH_RESPONSE_TYPE_CODE,
    OAUTH_PARAM_REDIRECT_URI,
    OAUTH_PAYLOAD_CLIENT_ID,
    OAUTH_PAYLOAD_CLIENT_SECRET,
    OAUTH_PAYLOAD_CODE,
    OAUTH_PAYLOAD_REDIRECT_URI,
    HEADER_CONTENT_TYPE,
    CONTENT_TYPE_JSON,
)

class CloverOAuthService:
    def get_authorize_url(self):
        params = {
            OAUTH_PARAM_CLIENT_ID: settings.CLOVER_CLIENT_ID,
            OAUTH_PARAM_RESPONSE_TYPE: OAUTH_RESPONSE_TYPE_CODE,
            OAUTH_PARAM_REDIRECT_URI: settings.CLOVER_REDIRECT_URI
        }
        return f"{settings.CLOVER_AUTH_BASE_URL}{OAUTH_AUTHORIZE_ENDPOINT}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str, merchant_id: str | None = None):
        token_url = f"{settings.CLOVER_API_BASE_URL}{OAUTH_TOKEN_ENDPOINT}"

        payload = {
            OAUTH_PAYLOAD_CLIENT_ID: settings.CLOVER_CLIENT_ID,
            OAUTH_PAYLOAD_CLIENT_SECRET: settings.CLOVER_CLIENT_SECRET,
            OAUTH_PAYLOAD_CODE: code,
            OAUTH_PAYLOAD_REDIRECT_URI: settings.CLOVER_REDIRECT_URI
        }

        headers = {
            HEADER_CONTENT_TYPE: CONTENT_TYPE_JSON
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, json=payload, headers=headers)

        response.raise_for_status()
        token_data = response.json()

        if merchant_id:
            token_data["merchant_id"] = merchant_id

        token_store.save_token(token_data)
        return token_data

clover_oauth_service = CloverOAuthService()