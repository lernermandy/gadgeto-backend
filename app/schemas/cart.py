from pydantic import BaseModel

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemUpdate(BaseModel):
    quantity: int

class CartOutItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    class Config:
        from_attributes = True

class CartOut(BaseModel):
    id: int
    status: str
    items: list[CartOutItem]
    class Config:
        from_attributes = True

