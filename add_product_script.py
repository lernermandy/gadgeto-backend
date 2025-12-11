from app.db.session import SessionLocal
from app.models.product import Product

def add_product():
    db = SessionLocal()
    sku = "SAMSUNG-S24-FE-BLUE"
    try:
        product = db.query(Product).filter(Product.sku == sku).first()
        
        data = {
            "sku": sku, 
            "name": "Samsung Galaxy S24 FE 5G (Blue, 128 GB) (8 GB RAM)", 
            "category": "Smartphone", 
            "price": 31999.0, 
            "battery_capacity": "4700 mAh", 
            "primary_camera": "50MP + 12MP | 10MP Front Camera", 
            "image_url": "/web/assets/images/samsung-s24-fe.png",
            "stock": 10,
            "description": "Highlights:\n- 8 GB RAM | 128 GB ROM\n- 17.02 cm (6.7 inch) Full HD+ Display\n- 50MP + 12MP | 10MP Front Camera\n- 4700 mAh Battery\n- Exynos 2400e Processor"
        }

        if product:
            print(f"Updating existing product {sku}")
            for key, value in data.items():
                setattr(product, key, value)
        else:
            print(f"Creating new product {sku}")
            product = Product(**data)
            db.add(product)
        
        db.commit()
        print("Product saved successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_product()
