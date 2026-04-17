from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer
from app.core.database import Base


class MerchantToken(Base):
    __tablename__ = "merchant_tokens"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    merchant_id = Column(String(255), unique=True, nullable=False, index=True)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    token_type = Column(String(50), default="Bearer", nullable=False)
    expires_in = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<MerchantToken merchant_id={self.merchant_id}>"
