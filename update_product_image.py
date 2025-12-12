from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.product import Product

def update_samsung_image():
    db: Session = SessionLocal()
    try:
        # Find the Samsung product
        # The SKU in init_db.py was "SAMSUNG-S24-FE-BLUE"
        product = db.query(Product).filter(Product.sku == "SAMSUNG-S24-FE-BLUE").first()
        if product:
            print(f"Found product: {product.name}")
            product.image_url = "/web/assets/images/samsung-s24.jpg"
            db.commit()
            print("Successfully updated Samsung S24 image URL.")
        else:
            print("Samsung S24 product not found in database.")
            
            # If not found, create it (just in case)
            print("Creating Samsung S24 product...")
            new_prod = Product(
                sku="SAMSUNG-S24-FE-BLUE", 
                name="Samsung Galaxy S24 FE 5G (Blue, 128 GB) (8 GB RAM)", 
                category="Mobile Phone", 
                price=31999.0, 
                battery_capacity="4700 mAh", 
                primary_camera="50MP + 12MP", 
                image_url="/web/assets/images/samsung-s24.jpg",
                stock=10
            )
            db.add(new_prod)
            db.commit()
            print("Created Samsung S24 product.")

    except Exception as e:
        print(f"Error updating product: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_samsung_image()
