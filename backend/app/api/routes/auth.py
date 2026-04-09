from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.services.clover_oauth_service import clover_oauth_service
from app.core.constants import (
    AUTH_ROUTER_PREFIX,
    AUTH_ROUTER_TAG,
    AUTH_START_ROUTE,
    AUTH_EXCHANGE_ROUTE,
)

router = APIRouter(prefix=AUTH_ROUTER_PREFIX, tags=[AUTH_ROUTER_TAG])

class CodeExchangeRequest(BaseModel):
    code: str
    merchant_id: str | None = None

@router.get(AUTH_START_ROUTE)
async def start_auth():
    auth_url = clover_oauth_service.get_authorize_url()
    return RedirectResponse(url=auth_url)

@router.post(AUTH_EXCHANGE_ROUTE)
async def exchange_code(payload: CodeExchangeRequest):
    try:
        token_data = await clover_oauth_service.exchange_code_for_token(
            payload.code,
            payload.merchant_id
        )
        return {
            "success": True,
            "message": "Clover connected successfully",
            "token_data": token_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))