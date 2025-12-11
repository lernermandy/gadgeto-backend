from sqlalchemy import Column, Integer, ForeignKey, String, Float
from ..db.base import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    provider = Column(String, default="cashfree")
    status = Column(String, default="created")
    session_id = Column(String, nullable=True)
    reference_id = Column(String, nullable=True)
    amount = Column(Float, default=0.0)

