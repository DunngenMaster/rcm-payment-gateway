import httpx
from app.core.config import settings
from app.db.token_store import token_store
from app.core.constants import (
    HEADER_AUTHORIZATION,
    HEADER_CONTENT_TYPE,
    AUTH_SCHEME_BEARER,
    CONTENT_TYPE_JSON,
    ERROR_NO_ACCESS_TOKEN,
)

class CloverClient:
    def __init__(self):
        self.base_url = settings.CLOVER_API_BASE_URL

    def _get_headers(self):
        access_token = token_store.get_access_token()

        if not access_token:
            raise Exception(ERROR_NO_ACCESS_TOKEN)

        return {
            HEADER_AUTHORIZATION: f"{AUTH_SCHEME_BEARER}{access_token}",
            HEADER_CONTENT_TYPE: CONTENT_TYPE_JSON,
        }

    async def get(self, endpoint: str, params: dict = None):
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)

        response.raise_for_status()
        return response.json()

    async def post(self, endpoint: str, json_data: dict):
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=json_data)

        response.raise_for_status()
        return response.json()

clover_client = CloverClient()