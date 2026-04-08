from fastapi import APIRouter
from app.core.constants import (
    HEALTH_ROUTER_TAG,
    HEALTH_ROUTE_PATH,
    HEALTH_STATUS_KEY,
    HEALTH_STATUS_OK,
)

router = APIRouter(tags=[HEALTH_ROUTER_TAG])

@router.get(HEALTH_ROUTE_PATH)
def health_check():
    return {HEALTH_STATUS_KEY: HEALTH_STATUS_OK}