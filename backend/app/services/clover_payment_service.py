from app.db.token_store import token_store
from app.core.config import settings
from app.core.database import SessionLocal
from app.db.models.merchant import Merchant
from app.db.models.payment import Payment
from app.db.models.order import Order
from app.db.models.enums import PaymentStatus
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
from sqlalchemy.orm import Session
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
        logger.info(f"[CHARGE] Starting charge creation for merchant: {merchant_id}")
        
        # Get the merchant's PRIVATE ecommerce key (needed for charging)
        db: Session = SessionLocal()
        try:
            merchant = db.query(Merchant).filter_by(clover_merchant_id=merchant_id).first()
            if not merchant or not merchant.ecommerce_private_token:
                error_msg = f"No ecommerce private token found for merchant {merchant_id}"
                logger.error(f"[CHARGE] ERROR: {error_msg}")
                raise ValueError(error_msg)
            
            ecommerce_key = merchant.ecommerce_private_token
            logger.info(f"[CHARGE] Retrieved merchant ecommerce key for: {merchant.merchant_name}")
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
            
            logger.info(f"[CHARGE] Calling Clover API: amount={amount}, source={source}, currency={currency}")
            logger.info(f"[CHARGE] URL: {url}")
            logger.info(f"[CHARGE] Database URL in use: {settings.DATABASE_URL if hasattr(settings, 'DATABASE_URL') else 'Not set'}")
            
            payload_dict = payload.to_dict()
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=payload_dict, headers=headers)
                
                response.raise_for_status()
                charge = response.json()
                
                logger.info(f"[CHARGE] Clover response successful: {charge}")
                logger.info(f"[CHARGE] Charge ID from Clover: {charge.get('id')}")
                
                # ========== INSERT INTO PAYMENTS TABLE ==========
                logger.info(f"[CHARGE] Starting payment insert into SQL database...")
                payment_db: Session = SessionLocal()
                try:
                    # First, ensure order exists in local database
                    order = payment_db.query(Order).filter_by(clover_order_id=charge.get("orderId")).first()
                    if not order:
                        logger.info(f"[CHARGE] Order not found for Clover order ID: {charge.get('orderId')}, checking merchant...")
                        # Create a minimal order record if it doesn't exist
                        # Use merchant.merchant_id (internal UUID) instead of clover merchant_id
                        order = Order(
                            merchant_id=merchant.merchant_id,
                            clover_order_id=charge.get("orderId"),
                            title=description or "Charge Order",
                            currency=currency,
                            total=amount / 100.0  # Convert cents to dollars
                        )
                        payment_db.add(order)
                        payment_db.flush()  # Get the order_id before committing
                        logger.info(f"[CHARGE] Created new order record: {order.order_id}")
                    else:
                        logger.info(f"[CHARGE] Found existing order: {order.order_id}")
                    
                    # Create payment record
                    # Use merchant.merchant_id (internal UUID) instead of clover merchant_id
                    payment = Payment(
                        merchant_id=merchant.merchant_id,
                        order_id=order.order_id,
                        clover_payment_id=charge.get("id"),
                        amount=amount / 100.0,  # Convert cents to dollars
                        currency=currency,
                        status=PaymentStatus.SUCCESS,
                        token=source
                    )
                    payment_db.add(payment)
                    logger.info(f"[CHARGE] Payment object created: {payment.payment_id}")
                    
                    # Commit the transaction
                    payment_db.commit()
                    logger.info(f"[CHARGE] Database commit successful")
                    logger.info(f"[CHARGE] Payment inserted: payment_id={payment.payment_id}, amount={amount/100.0}, status={PaymentStatus.SUCCESS}")
                    
                except Exception as db_error:
                    payment_db.rollback()
                    logger.error(f"[CHARGE] Database insert FAILED: {type(db_error).__name__} - {str(db_error)}")
                    logger.error(f"[CHARGE] Rollback executed")
                    raise
                finally:
                    payment_db.close()
                
                # Log transaction for audit trail
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
                logger.info(f"[CHARGE] Transaction logged to audit table")
                
                logger.info(f"[CHARGE] Charge flow complete")
                return charge
                
        except httpx.TimeoutException as e:
            error_detail = f"Clover API timeout: Request took too long. Check OAuth token validity and Clover API status."
            logger.error(f"[CHARGE] {error_detail}")
            raise ValueError(error_detail)
        except httpx.HTTPStatusError as e:
            error_detail = f"Clover API error: {e.response.status_code} - {e.response.text}"
            logger.error(f"[CHARGE] {error_detail}")
            raise ValueError(error_detail)
        except Exception as e:
            error_detail = f"Charge creation failed: {type(e).__name__} - {str(e)}"
            logger.error(f"[CHARGE] {error_detail}")
            raise ValueError(error_detail)

clover_payment_service = CloverPaymentService()