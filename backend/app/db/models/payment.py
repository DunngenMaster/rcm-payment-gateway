from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.db.models.enums import PaymentStatus


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    merchant_id = Column(String(36), ForeignKey("merchants.merchant_id"), nullable=False, index=True)
    order_id = Column(String(36), ForeignKey("orders.order_id"), nullable=False, index=True)
    clover_payment_id = Column(String(255), nullable=True, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    token = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    merchant = relationship("Merchant", back_populates="payments")
    order = relationship("Order", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.payment_id} - {self.status}>"
