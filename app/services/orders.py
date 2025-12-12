from sqlalchemy.orm import Session
from ..models.cart import Cart
from ..models.cart_item import CartItem
from ..models.order import Order
from ..models.order_item import OrderItem
from ..models.address import Address

class OrderService:
    def create_order_from_cart(self, db: Session, user_id: int, billing: dict, shipping: dict, payment_method: str = "cod"):
        cart = db.query(Cart).filter(Cart.user_id == user_id, Cart.status == "open").first()
        if not cart or not cart.items:
            return None
        order = Order(user_id=user_id, status="pending", payment_method=payment_method)
        db.add(order)
        db.commit()
        db.refresh(order)
        ba = Address(user_id=user_id, **billing)
        sa = Address(user_id=user_id, **shipping)
        db.add(ba)
        db.add(sa)
        db.commit()
        db.refresh(ba)
        db.refresh(sa)
        order.billing_address_id = ba.id
        order.shipping_address_id = sa.id
        total = 0.0
        for item in cart.items:
            oi = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity, price=item.price)
            db.add(oi)
            total += item.price * item.quantity
        order.total_amount = total
        
        if payment_method == "online":
            # Generate UPI Payment Link
            # format: upi://pay?pa={merchant_upi}&pn={merchant_name}&am={amount}&cu=INR&tn={transaction_note}
            merchant_upi = "jmandar0707@okhdfcbank"
            merchant_name = "mandar jadhav"
            transaction_note = f"Order #{order.id}"
            amount_str = f"{total:.2f}"
            order.upi_payment_link = f"upi://pay?pa={merchant_upi}&pn={merchant_name}&am={amount_str}&cu=INR&tn={transaction_note}"

        cart.status = "converted"
        db.add(order)
        db.add(cart)
        db.commit()
        db.refresh(order)
        return order
