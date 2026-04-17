from app.db.token_store import token_store
from app.core.config import settings
from app.core.database import SessionLocal
from app.db.models.merchant import Merchant
from app.core.constants import (
    ERROR_NO_ACCESS_TOKEN,
    ERROR_AMOUNT_SOURCE_REQUIRED,
    CLOVER_PAKMS_ENDPOINT,
    CLOVER_CHARGES_ENDPOINT,
    HEADER_AUTHORIZATION,
    HEADER_ACCEPT,
    HEADER_CONTENT_TYPE,
    HEADER_X_FORWARDED_FOR,
    CONTENT_TYPE_JSON,
    AUTH_SCHEME_BEARER,
    TRANSACTION_STATUS_SUCCESS,
    TRANSACTION_TYPE_CHARGE,
    DEFAULT_CHARGE_CURRENCY,
    DEFAULT_CHARGE_DESCRIPTION,
)
from app.models import ChargePayload
from app.db.transaction_store import save_transaction
import httpx
import logging

logger = logging.getLogger(__name__)


class CloverPaymentService:
    
    def _get_merchant_ecommerce_key(self, merchant_id: str) -> str | None:
        """Get ecommerce public key from merchants table"""
        db = SessionLocal()
        try:
            merchant = db.query(Merchant).filter_by(clover_merchant_id=merchant_id).first()
            if merchant and merchant.ecommerce_public_token:
                return merchant.ecommerce_public_token
            return None
        finally:
            db.close()
    
    async def get_ecommerce_key(self, merchant_id: str = None):
        """Get ecommerce key for a specific merchant"""
        # Try to get from merchants table first
        if merchant_id:
            key = self._get_merchant_ecommerce_key(merchant_id)
            if key:
                return {"apiAccessKey": key}
        
        # Fallback to Clover API if not in table
        access_token = token_store.get_access_token(merchant_id)
        if not access_token:
            raise ValueError(ERROR_NO_ACCESS_TOKEN)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.CLOVER_ECOMMERCE_BASE_URL}{CLOVER_PAKMS_ENDPOINT}",
                headers={
                    HEADER_AUTHORIZATION: f"{AUTH_SCHEME_BEARER}{access_token}",
                    HEADER_ACCEPT: CONTENT_TYPE_JSON
                }
            )
            response.raise_for_status()
            return response.json()

    async def create_charge(self, amount: int, source: str, currency: str = DEFAULT_CHARGE_CURRENCY, 
                           description: str = DEFAULT_CHARGE_DESCRIPTION, merchant_id: str = None):
        """Create charge for a specific merchant"""
        logger.info(f"Creating charge for merchant: {merchant_id}")
        
        # Get the merchant's PRIVATE ecommerce key (needed for charging)
        db: Session = SessionLocal()
        try:
            merchant = db.query(Merchant).filter_by(clover_merchant_id=merchant_id).first()
            if not merchant or not merchant.ecommerce_private_token:
                error_msg = f"No ecommerce private token found for merchant {merchant_id}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            ecommerce_key = merchant.ecommerce_private_token
        finally:
            db.close()
        
        if not amount or not source:
            raise ValueError(ERROR_AMOUNT_SOURCE_REQUIRED)
        
        try:
            payload = ChargePayload(amount, source, currency, description)
            
            url = f"{settings.CLOVER_ECOMMERCE_BASE_URL}{CLOVER_CHARGES_ENDPOINT}"
            headers = {
                HEADER_AUTHORIZATION: f"{AUTH_SCHEME_BEARER}{ecommerce_key}",
                HEADER_ACCEPT: CONTENT_TYPE_JSON,
                HEADER_CONTENT_TYPE: CONTENT_TYPE_JSON,
                HEADER_X_FORWARDED_FOR: "127.0.0.1"
            }
            
            logger.info(f"Creating charge: amount={amount}, source={source}")
            
            payload_dict = payload.to_dict()
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=payload_dict, headers=headers)
                
                response.raise_for_status()
                charge = response.json()
                
                save_transaction({
                    "type": TRANSACTION_TYPE_CHARGE,
                    "amount": amount,
                    "source": source,
                    "currency": currency,
                    "description": description,
                    "status": TRANSACTION_STATUS_SUCCESS,
                    "charge_id": charge.get("id"),
                    "clover_response": charge,
                    "merchant_id": merchant_id
                })
                
                logger.info(f"Charge created successfully: {charge.get('id')}")
                return charge
        except httpx.TimeoutException as e:
            error_detail = f"Clover API timeout: Request took too long. Check OAuth token validity and Clover API status."
            logger.error(error_detail)
            raise ValueError(error_detail)
        except httpx.HTTPStatusError as e:
            error_detail = f"Clover API error: {e.response.status_code} - {e.response.text}"
            logger.error(error_detail)
            raise ValueError(error_detail)
        except Exception as e:
            error_detail = f"Charge creation failed: {type(e).__name__} - {str(e)}"
            logger.error(error_detail)
            raise ValueError(error_detail)

clover_payment_service = CloverPaymentService()