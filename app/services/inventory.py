from sqlalchemy.orm import Session
from ..models.product import Product

class InventoryService:
    def reduce_stock(self, db: Session, product_id: int, quantity: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False
        if product.stock < quantity:
            return False
        product.stock -= quantity
        db.add(product)
        db.commit()
        db.refresh(product)
        return True
