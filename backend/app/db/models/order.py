from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    merchant_id = Column(String(36), ForeignKey("merchants.merchant_id"), nullable=False, index=True)
    clover_order_id = Column(String(255), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    total = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    merchant = relationship("Merchant", back_populates="orders")
    line_items = relationship("LineItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order {self.order_id}>"
