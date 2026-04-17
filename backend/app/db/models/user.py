from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    merchant_id = Column(String(36), ForeignKey("merchants.merchant_id"), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    merchant = relationship("Merchant", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"
