from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...schemas.payment import PaymentCreate, PaymentOut, PaymentWebhook, PaymentSessionOut
from ...services.cashfree import CashfreeService
from ...core.config import settings
from ...services.inventory import InventoryService
from ...models.payment import Payment
from ...models.order import Order
from ...models.order_item import OrderItem

router = APIRouter(prefix="/payments", tags=["payments"])
service = CashfreeService()
inventory = InventoryService()

@router.post("/create-session", response_model=PaymentSessionOut)
def create_session(payload: PaymentCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == payload.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    p = Payment(order_id=order.id, amount=payload.amount)
    db.add(p)
    db.commit()
    db.refresh(p)
    res = service.create_session(order.id, payload.amount)
    p.session_id = res.get("session_id")
    p.reference_id = res.get("reference_id")
    p.status = "pending"
    db.add(p)
    db.commit()
    db.refresh(p)
    return PaymentSessionOut(
        id=p.id,
        status=p.status,
        session_id=p.session_id,
        reference_id=p.reference_id,
        amount=p.amount,
        upi_link=res.get("upi_link"),
        vpa=settings.UPI_VPA,
        name=settings.UPI_NAME,
    )

@router.post("/webhook")
def webhook(payload: PaymentWebhook, db: Session = Depends(get_db)):
    res = service.verify_payment(payload.reference_id)
    if res.get("status") != "paid":
        raise HTTPException(status_code=400, detail="Payment not verified")
    order = db.query(Order).filter(Order.id == payload.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "paid"
    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    for it in items:
        inventory.reduce_stock(db, it.product_id, it.quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"status": "ok"}

@router.post("/cod")
def cod_payment(payload: PaymentWebhook, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == payload.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "confirmed_cod" 
    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    for it in items:
        inventory.reduce_stock(db, it.product_id, it.quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"status": "ok"}
