from sqlalchemy import Column, Integer, ForeignKey
from ..db.base import Base

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    stock = Column(Integer, default=0)

