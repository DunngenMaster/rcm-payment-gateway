import httpx
from urllib.parse import urlencode
from app.core.config import settings
from app.db.token_store import token_store

OAUTH_AUTHORIZE_ENDPOINT = "/oauth/v2/authorize"
OAUTH_TOKEN_ENDPOINT = "/oauth/v2/token"

class CloverOAuthService:
    def get_authorize_url(self):
        params = {
            "client_id": settings.CLOVER_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": settings.CLOVER_REDIRECT_URI
        }
        return f"{settings.CLOVER_AUTH_BASE_URL}{OAUTH_AUTHORIZE_ENDPOINT}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str, merchant_id: str | None = None):
        token_url = f"{settings.CLOVER_API_BASE_URL}{OAUTH_TOKEN_ENDPOINT}"

        payload = {
            "client_id": settings.CLOVER_CLIENT_ID,
            "client_secret": settings.CLOVER_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.CLOVER_REDIRECT_URI
        }

        headers = {
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, json=payload, headers=headers)

        print("TOKEN URL:", token_url)
        print("TOKEN STATUS:", response.status_code)
        print("TOKEN RESPONSE:", response.text)

        response.raise_for_status()

        token_data = response.json()

        if merchant_id:
            token_data["merchant_id"] = merchant_id

        token_store.save_token(token_data)
        return token_data

clover_oauth_service = CloverOAuthService()