from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from app.core.database import Base


class Merchant(Base):
    __tablename__ = "merchants"

    merchant_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    clover_merchant_id = Column(String(255), unique=True, nullable=False, index=True)
    clover_access_token = Column(LargeBinary, nullable=False)
    merchant_name = Column(String(255), nullable=True)
    ecommerce_public_token = Column(String(255), nullable=True)
    ecommerce_private_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="merchant", uselist=False)
    orders = relationship("Order", back_populates="merchant", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="merchant", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Merchant {self.merchant_name}>"
