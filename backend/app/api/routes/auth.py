from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from app.services.clover_oauth_service import clover_oauth_service
from app.core.config import settings
from app.core.constants import (
    AUTH_ROUTER_PREFIX,
    AUTH_ROUTER_TAG,
    AUTH_START_ROUTE,
    AUTH_CALLBACK_ROUTE,
    AUTH_SUCCESS_QUERY_PARAM,
)

router = APIRouter(prefix=AUTH_ROUTER_PREFIX, tags=[AUTH_ROUTER_TAG])

@router.get(AUTH_START_ROUTE)
async def start_auth():
    auth_url = clover_oauth_service.get_authorize_url()
    return RedirectResponse(url=auth_url)

@router.get(AUTH_CALLBACK_ROUTE)
async def auth_callback(code: str = Query(...)):
    try:
        await clover_oauth_service.exchange_code_for_token(code)
        return RedirectResponse(url=f"{settings.FRONTEND_URL}{AUTH_SUCCESS_QUERY_PARAM}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))