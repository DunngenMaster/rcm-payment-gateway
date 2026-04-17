from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Float
from app.core.database import Base


class TransactionLog(Base):
    __tablename__ = "transaction_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    merchant_id = Column(String(255), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)
    status = Column(String(50), default="pending", nullable=False)
    amount = Column(Float, nullable=True)
    order_id = Column(String(255), nullable=True, index=True)
    clover_reference_id = Column(String(255), nullable=True, index=True)
    response_payload = Column(Text, nullable=True)  # Store as JSON string
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return f"<TransactionLog merchant_id={self.merchant_id} type={self.type}>"
