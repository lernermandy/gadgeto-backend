from pydantic import BaseModel

class ProductBase(BaseModel):
    sku: str
    name: str
    category: str
    capacity_litres: int | None = None
    temperature_range: str | None = None
    humidity_range: str | None = None
    price: float
    description: str | None = None
    image_url: str | None = None
    battery_capacity: str | None = None
    primary_camera: str | None = None
    stock: int | None = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    capacity_litres: int | None = None
    temperature_range: str | None = None
    humidity_range: str | None = None
    price: float | None = None
    description: str | None = None
    image_url: str | None = None
    battery_capacity: str | None = None
    primary_camera: str | None = None
    stock: int | None = None

class ProductOut(ProductBase):
    id: int
    class Config:
        from_attributes = True
 
