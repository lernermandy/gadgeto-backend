from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...core.security import require_admin
from ...models.order import Order
from ...models.user import User
from ...models.product import Product

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/ping")
def ping(user = Depends(require_admin)):
    return {"ok": True}

@router.get("/orders")
def all_orders(db: Session = Depends(get_db), user = Depends(require_admin)):
    orders = db.query(Order).order_by(Order.id.desc()).all()
    total = sum(o.total_amount or 0 for o in orders)
    return {"total_sales": total, "count": len(orders), "orders": orders}

@router.get("/customers")
def customers(db: Session = Depends(get_db), user = Depends(require_admin)):
    users = db.query(User).order_by(User.id.desc()).all()
    return {"count": len(users), "users": users}

@router.get("/inventory")
def inventory(db: Session = Depends(get_db), user = Depends(require_admin)):
    products = db.query(Product).all()
    return [{"id": p.id, "sku": p.sku, "name": p.name, "stock": p.stock, "price": p.price} for p in products]
