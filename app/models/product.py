from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    capacity_litres = Column(Integer, nullable=True)
    temperature_range = Column(String, nullable=True)
    humidity_range = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    battery_capacity = Column(String, nullable=True)
    primary_camera = Column(String, nullable=True)
    stock = Column(Integer, default=0)
