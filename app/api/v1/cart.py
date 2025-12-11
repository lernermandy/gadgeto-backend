from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models.cart import Cart
from ...models.cart_item import CartItem
from ...models.product import Product
from ...schemas.cart import CartItemCreate, CartItemUpdate, CartOut

router = APIRouter(prefix="/cart", tags=["cart"])

def get_or_create_cart(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id, Cart.status == "open").first()
    if not cart:
        cart = Cart(user_id=user_id, status="open")
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.get("/{user_id}", response_model=CartOut)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart = get_or_create_cart(db, user_id)
    return cart

@router.post("/{user_id}/items", response_model=CartOut)
def add_to_cart(user_id: int, payload: CartItemCreate, db: Session = Depends(get_db)):
    cart = get_or_create_cart(db, user_id)
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product.id).first()
    if item:
        item.quantity += payload.quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=product.id, quantity=payload.quantity, price=product.price)
        db.add(item)
    db.commit()
    db.refresh(cart)
    return cart

@router.put("/{user_id}/items/{item_id}", response_model=CartOut)
def update_item(user_id: int, item_id: int, payload: CartItemUpdate, db: Session = Depends(get_db)):
    cart = get_or_create_cart(db, user_id)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.quantity = payload.quantity
    db.add(item)
    db.commit()
    db.refresh(cart)
    return cart

@router.delete("/{user_id}/items/{item_id}", response_model=CartOut)
def remove_item(user_id: int, item_id: int, db: Session = Depends(get_db)):
    cart = get_or_create_cart(db, user_id)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    db.refresh(cart)
    return cart
