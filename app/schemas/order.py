from pydantic import BaseModel

class AddressBase(BaseModel):
    line1: str
    line2: str | None = None
    city: str
    state: str
    postal_code: str
    country: str

class OrderCreate(BaseModel):
    billing_address: AddressBase
    shipping_address: AddressBase
    payment_method: str = "cod"

class OrderOutItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderOut(BaseModel):
    id: int
    status: str
    total_amount: float
    payment_method: str
    upi_payment_link: str | None = None
    items: list[OrderOutItem] | None = None
    class Config:
        from_attributes = True
