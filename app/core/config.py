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
    GOOGLE_CLIENT_ID = "95703734000-5g9099b15uh4md9hav06ppe6mvj8apvd.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "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"
    GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "https://gadgeto.vercel.app/auth/google/callback")

settings = Settings()
