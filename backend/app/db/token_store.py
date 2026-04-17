import json
from pathlib import Path
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.constants import OAUTH_PARAM_MERCHANT_ID, TOKEN_JSON_KEY_ACCESS_TOKEN
from app.db.models.merchant_token import MerchantToken
from datetime import datetime


class TokenStore:
    """Store and retrieve encrypted merchant OAuth tokens from MySQL"""

    def __init__(self):
        if not settings.TOKEN_ENCRYPTION_KEY:
            raise ValueError("TOKEN_ENCRYPTION_KEY not set in environment variables")
        self.cipher = Fernet(settings.TOKEN_ENCRYPTION_KEY.encode())

    def _encrypt_token(self, token_str: str) -> str:
        """Encrypt token string"""
        return self.cipher.encrypt(token_str.encode()).decode()

    def _decrypt_token(self, encrypted_token: str) -> str:
        """Decrypt token string"""
        return self.cipher.decrypt(encrypted_token.encode()).decode()

    def save_token(self, token_data: dict):
        """Save or update merchant token in database with encryption"""
        db: Session = SessionLocal()
        try:
            merchant_id = token_data.get(OAUTH_PARAM_MERCHANT_ID)
            if not merchant_id:
                raise ValueError("merchant_id is required in token_data")

            # Encrypt the access token
            encrypted_access_token = self._encrypt_token(token_data.get("access_token", ""))

            # Check if token already exists
            existing = db.query(MerchantToken).filter_by(merchant_id=merchant_id).first()

            if existing:
                # Update existing token
                existing.access_token = encrypted_access_token
                existing.refresh_token = token_data.get("refresh_token")
                existing.token_type = token_data.get("token_type", "Bearer")
                existing.expires_in = token_data.get("expires_in")
                existing.updated_at = datetime.utcnow()
            else:
                # Create new token
                token = MerchantToken(
                    merchant_id=merchant_id,
                    access_token=encrypted_access_token,
                    refresh_token=token_data.get("refresh_token"),
                    token_type=token_data.get("token_type", "Bearer"),
                    expires_in=token_data.get("expires_in"),
                )
                db.add(token)

            db.commit()
        finally:
            db.close()

    def load_token(self, merchant_id: str = None) -> dict | None:
        """Load and decrypt token for a merchant. If merchant_id is None, gets first token."""
        db: Session = SessionLocal()
        try:
            if merchant_id:
                token_obj = db.query(MerchantToken).filter_by(merchant_id=merchant_id).first()
            else:
                # Backwards compatibility: get first token
                token_obj = db.query(MerchantToken).first()

            if not token_obj:
                return None

            # Decrypt the access token
            decrypted_access_token = self._decrypt_token(token_obj.access_token)

            return {
                OAUTH_PARAM_MERCHANT_ID: token_obj.merchant_id,
                "access_token": decrypted_access_token,
                "refresh_token": token_obj.refresh_token,
                "token_type": token_obj.token_type,
                "expires_in": token_obj.expires_in,
            }
        except Exception as e:
            print(f"Error loading token: {e}")
            return None
        finally:
            db.close()

    def get_access_token(self, merchant_id: str = None) -> str | None:
        """Get decrypted access token for a merchant"""
        token_data = self.load_token(merchant_id)
        if not token_data:
            return None
        return token_data.get(TOKEN_JSON_KEY_ACCESS_TOKEN)

    def get_merchant_id(self) -> str | None:
        """Get merchant_id from first token (backwards compatibility)"""
        token_data = self.load_token()
        if not token_data:
            return None
        return token_data.get(OAUTH_PARAM_MERCHANT_ID)

    def delete_token(self, merchant_id: str) -> None:
        """Delete token for a merchant"""
        db: Session = SessionLocal()
        try:
            db.query(MerchantToken).filter_by(merchant_id=merchant_id).delete()
            db.commit()
        finally:
            db.close()

    def get_merchant_ecommerce_key(self, clover_merchant_id: str) -> str | None:
        """Get ecommerce public token for a merchant from merchants table"""
        from app.db.models.merchant import Merchant
        db: Session = SessionLocal()
        try:
            merchant = db.query(Merchant).filter_by(clover_merchant_id=clover_merchant_id).first()
            if merchant:
                return merchant.ecommerce_public_token
            return None
        finally:
            db.close()


token_store = TokenStore()

