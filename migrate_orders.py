import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "ecommerce.db")

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN payment_method TEXT DEFAULT 'cod'")
        print("Added payment_method column")
    except sqlite3.OperationalError as e:
        print(f"payment_method column might already exist: {e}")

    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN upi_payment_link TEXT")
        print("Added upi_payment_link column")
    except sqlite3.OperationalError as e:
        print(f"upi_payment_link column might already exist: {e}")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        migrate()
    else:
        print("Database not found, skipping migration (will be created on startup)")
