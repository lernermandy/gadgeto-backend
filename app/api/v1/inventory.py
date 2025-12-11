from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models.product import Product

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/", response_model=list[dict])
def list_inventory(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [{"id": p.id, "sku": p.sku, "stock": p.stock} for p in products]
