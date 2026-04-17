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
        self._current_merchant_id = None  # For single-merchant backwards compatibility

    def _get_headers(self, merchant_id: str = None):
        """Get headers with authorization for a specific merchant"""
        # Use provided merchant_id, fall back to current, then fall back to first merchant
        access_token = token_store.get_access_token(merchant_id)
        if not access_token:
            raise Exception(ERROR_NO_ACCESS_TOKEN)

        return {
            HEADER_AUTHORIZATION: f"{AUTH_SCHEME_BEARER}{access_token}",
            HEADER_CONTENT_TYPE: CONTENT_TYPE_JSON
        }

    def set_merchant_id(self, merchant_id: str):
        """Set merchant context for backwards compatibility"""
        self._current_merchant_id = merchant_id

    def get_merchant_id(self, merchant_id: str = None) -> str:
        """Get merchant ID - use provided, fall back to current, then to first from DB"""
        if merchant_id:
            return merchant_id
        
        if self._current_merchant_id:
            return self._current_merchant_id
        
        # Fall back to first merchant from token store (backwards compatibility)
        merchant_id = token_store.get_merchant_id()
        if not merchant_id:
            raise Exception("Merchant ID not found. Please authenticate with Clover first.")
        
        return merchant_id

    async def post(self, endpoint: str, json_data: dict, merchant_id: str = None):
        """Make POST request to Clover API for a specific merchant"""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(merchant_id)

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=json_data)

        response.raise_for_status()
        return response.json()

    async def get(self, endpoint: str, merchant_id: str = None):
        """Make GET request to Clover API for a specific merchant"""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(merchant_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        response.raise_for_status()
        return response.json()

    async def delete(self, endpoint: str, merchant_id: str = None):
        """Make DELETE request to Clover API for a specific merchant"""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(merchant_id)

        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers)

        response.raise_for_status()
        return response.json()

clover_client = CloverClient()