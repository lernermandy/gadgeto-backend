from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...schemas.order import OrderCreate, OrderOut
from ...services.orders import OrderService
from ...models.order import Order

router = APIRouter(prefix="/orders", tags=["orders"])
service = OrderService()

@router.post("/{user_id}", response_model=OrderOut)
def create_order(user_id: int, payload: OrderCreate, db: Session = Depends(get_db)):
    order = service.create_order_from_cart(db, user_id, payload.billing_address.dict(), payload.shipping_address.dict(), payload.payment_method)
    if not order:
        raise HTTPException(status_code=400, detail="Cart empty")
    return order

@router.get("/{user_id}", response_model=list[OrderOut])
def list_orders(user_id: int, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.id.desc()).all()
