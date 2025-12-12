import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./ecommerce.db")
    CASHFREE_APP_ID = os.environ.get("CASHFREE_APP_ID", "")
    CASHFREE_SECRET_KEY = os.environ.get("CASHFREE_SECRET_KEY", "")
    CASHFREE_ENV = os.environ.get("CASHFREE_ENV", "sandbox")
    UPI_VPA = "jmandar0707@okhdfcbank"
    UPI_NAME = "mandar jadhav"
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://127.0.0.1:8001/auth/google/callback")

settings = Settings()
