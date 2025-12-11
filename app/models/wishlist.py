from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from ..db.base import Base

class Wishlist(Base):
    __tablename__ = "wishlist"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uix_wishlist_user_product"),)
