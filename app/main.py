from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, Response
from pathlib import Path
from .api.v1 import users, auth, products, cart, wishlist, orders, payments, inventory, admin
from .db.init_db import init_db, seed_products, seed_demo_user

app = FastAPI(title="Gadgeto API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()
    seed_demo_user()
    seed_products()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(wishlist.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(inventory.router)
app.include_router(admin.router)

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/web", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="web")

@app.get("/")
def root():
    return RedirectResponse(url="/web/index.html")

@app.get("/auth/google-client-id")
def get_google_client_id():
    import os
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    return {"client_id": client_id}

@app.get("/@vite/client")
def vite_client_stub():
    return Response("/* vite client stub */", media_type="application/javascript")

