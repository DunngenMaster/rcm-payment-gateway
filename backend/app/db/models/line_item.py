from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base


class LineItem(Base):
    __tablename__ = "line_items"

    line_item_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    order_id = Column(String(36), ForeignKey("orders.order_id"), nullable=False, index=True)
    merchant_id = Column(String(36), ForeignKey("merchants.merchant_id"), nullable=False, index=True)
    clover_line_item_id = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    order = relationship("Order", back_populates="line_items")

    def __repr__(self):
        return f"<LineItem {self.name}>"
