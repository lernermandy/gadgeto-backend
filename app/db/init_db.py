from .session import engine, SessionLocal
from .base import Base
from ..models.product import Product
from ..models.user import User
from ..core.security import get_password_hash
from ..models.password_reset import PasswordReset

def init_db():
    Base.metadata.create_all(bind=engine)

def seed_demo_user():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "demo@example.com").first():
            u = User(email="demo@example.com", hashed_password=get_password_hash("demo123"), full_name="Demo User", is_admin=True)
            db.add(u)
            db.commit()
    finally:
        db.close()

def seed_products():
    db = SessionLocal()
    try:
        count = db.query(Product).count()
        if count == 0:
            data = [
                {"sku": "EGWHC171", "name": "Walk-In Humidity Chamber – EGWHC171", "category": "Stability Chamber", "capacity_litres": 4500, "temperature_range": "10°C – 85°C", "humidity_range": "20% – 95% RH", "price": 650000.0, "image_url": "/web/assets/images/EGWHC171.svg"},
                {"sku": "EGPGC4500", "name": "Walk-In Plant Growth Chamber", "category": "Growth Chamber", "capacity_litres": 4500, "temperature_range": "Configurable", "humidity_range": "Available", "price": 720000.0, "image_url": "/web/assets/images/EGPGC4500.svg"},
                {"sku": "EGWCC190", "name": "Booster Cooling Walk-In Chamber – EGWCC190", "category": "Cooling Chamber", "capacity_litres": 5400, "temperature_range": "2°C – 8°C", "price": 580000.0, "image_url": "/web/assets/images/EGWCC190.svg"},
                {"sku": "EGWIC190", "name": "Walk-In Incubator Chamber – EGWIC190", "category": "Incubator", "capacity_litres": 5400, "temperature_range": "+5°C – 75°C", "price": 420000.0, "image_url": "/web/assets/images/EGWIC190.svg"},
                {"sku": "EGHC7S/M", "name": "Humidity Stability Chamber – EGHC7S/M", "category": "Stability Chamber", "capacity_litres": 200, "temperature_range": "10°C – 60°C", "humidity_range": "40% – 95% RH", "price": 140000.0, "image_url": "/web/assets/images/EGHC7S-M.svg"},
                {"sku": "EGBI7S/M", "name": "BOD Incubator Chamber – EGBI7S/M", "category": "Incubator", "capacity_litres": 200, "temperature_range": "+5°C – 60°C", "price": 125000.0},
                {"sku": "EGCC7S/M", "name": "Cooling Chamber – EGCC7S/M", "category": "Cooling Chamber", "capacity_litres": 200, "temperature_range": "2°C – 8°C", "price": 175000.0},
                {"sku": "EGFTC7S/M", "name": "Freeze-Thaw Chamber – EGFTC7S/M", "category": "Freeze & Thermal Cycle Testing", "capacity_litres": 200, "temperature_range": "−30°C to +70°C", "price": 295000.0},
                {"sku": "EGLI7S/M", "name": "Lab Incubator – EGLI7S/M", "category": "Incubator", "capacity_litres": 200, "temperature_range": "Ambient +5°C to 75°C", "price": 110000.0},
                {"sku": "EGDF7S/M", "name": "Deep Freezer Chamber – EGDF7S/M", "category": "Deep Freezer", "capacity_litres": 200, "temperature_range": "−30°C to −5°C", "price": 220000.0},
                {"sku": "SAMSUNG-S24-FE-BLUE", "name": "Samsung Galaxy S24 FE 5G (Blue, 128 GB) (8 GB RAM)", "category": "Mobile Phone", "price": 31999.0, "battery_capacity": "4700 mAh", "primary_camera": "50MP + 12MP", "image_url": "/web/assets/images/samsung-s24-fe.png"},
            ]
            for p in data:
                prod = Product(**p)
                prod.stock = 10
                db.add(prod)
        db.commit()
    finally:
        db.close()
