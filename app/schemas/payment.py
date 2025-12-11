from pydantic import BaseModel

class PaymentCreate(BaseModel):
    order_id: int
    amount: float

class PaymentOut(BaseModel):
    id: int
    status: str
    session_id: str | None = None
    reference_id: str | None = None
    amount: float
    class Config:
        from_attributes = True

class PaymentWebhook(BaseModel):
    reference_id: str
    order_id: int

class PaymentSessionOut(BaseModel):
    id: int
    status: str
    session_id: str | None = None
    reference_id: str | None = None
    amount: float
    upi_link: str | None = None
    vpa: str | None = None
    name: str | None = None
