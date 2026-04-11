from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.models import CodeExchangeRequest
from app.api.handlers import AuthHandler
from app.core.constants import (
    AUTH_ROUTER_PREFIX,
    AUTH_ROUTER_TAG,
    AUTH_START_ROUTE,
    AUTH_EXCHANGE_ROUTE,
    HTTP_STATUS_INTERNAL_SERVER_ERROR,
)

auth_handler = AuthHandler()
router = APIRouter(prefix=AUTH_ROUTER_PREFIX, tags=[AUTH_ROUTER_TAG])


@router.get(AUTH_START_ROUTE)
async def start_auth():
    auth_url = await auth_handler.start_auth()
    return RedirectResponse(url=auth_url)


@router.post(AUTH_EXCHANGE_ROUTE)
async def exchange_code(payload: CodeExchangeRequest):
    try:
        return await auth_handler.exchange_code(payload)
    except Exception as e:
        raise HTTPException(status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/status")
async def check_status():
    return await auth_handler.check_connection()
