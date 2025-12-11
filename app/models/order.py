from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.base import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")
    total_amount = Column(Float, default=0.0)
    billing_address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    shipping_address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    payment_method = Column(String, default="cod")
    upi_payment_link = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
