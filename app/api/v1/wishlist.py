from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models.wishlist import Wishlist
from ...schemas.wishlist import WishlistCreate, WishlistOut

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

@router.get("/{user_id}", response_model=list[WishlistOut])
def list_wishlist(user_id: int, db: Session = Depends(get_db)):
    return db.query(Wishlist).filter(Wishlist.user_id == user_id).all()

@router.post("/{user_id}", response_model=WishlistOut)
def add_wishlist(user_id: int, payload: WishlistCreate, db: Session = Depends(get_db)):
    item = Wishlist(user_id=user_id, product_id=payload.product_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{user_id}/{product_id}")
def remove_wishlist(user_id: int, product_id: int, db: Session = Depends(get_db)):
    item = db.query(Wishlist).filter(Wishlist.user_id == user_id, Wishlist.product_id == product_id).first()
    if item:
        db.delete(item)
        db.commit()
    return {"deleted": True}
