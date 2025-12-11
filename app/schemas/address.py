from pydantic import BaseModel

class AddressCreate(BaseModel):
    line1: str
    line2: str | None = None
    city: str
    state: str
    postal_code: str
    country: str
