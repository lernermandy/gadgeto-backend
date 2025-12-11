from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...schemas.user import UserCreate, UserLogin, UserOut
from ...core.security import get_password_hash, verify_password, create_access_token
from ...models.user import User
from ...models.password_reset import PasswordReset
from ...schemas.auth import ForgotPasswordRequest, ResetPasswordRequest, GoogleAuthRequest
from ...core.config import settings
import httpx
from fastapi.responses import RedirectResponse
import base64
import uuid
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, hashed_password=get_password_hash(payload.password), full_name=payload.full_name or "")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/forgot")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        return {"sent": True}
    reset = PasswordReset(user_id=user.id, token=str(uuid.uuid4()))
    db.add(reset)
    db.commit()
    db.refresh(reset)
    return {"sent": True, "token": reset.token}

@router.post("/reset")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    pr = db.query(PasswordReset).filter(PasswordReset.token == payload.token).first()
    if not pr or pr.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == pr.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = get_password_hash(payload.new_password)
    db.add(user)
    db.delete(pr)
    db.commit()
    return {"reset": True}

@router.post("/google")
def google_login(payload: GoogleAuthRequest, db: Session = Depends(get_db)):
    if not settings.GOOGLE_CLIENT_ID:
        email = payload.email or "demo.google@example.com"
        name = "Google User"
    else:
        try:
            r = httpx.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": payload.id_token}, timeout=10)
            if r.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid Google token")
            info = r.json()
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid Google token")
        aud = info.get("aud")
        if settings.GOOGLE_CLIENT_ID and aud != settings.GOOGLE_CLIENT_ID:
            raise HTTPException(status_code=401, detail="Client mismatch")
        email = info.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email missing")
        name = info.get("name") or f"{info.get('given_name','')} {info.get('family_name','')}".strip()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, hashed_password=get_password_hash("oauth"), full_name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
    token = create_access_token({"sub": str(user.id), "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/google/initiate")
def google_initiate(next: str = "/web/index.html"):
    if not settings.GOOGLE_CLIENT_ID:
        return RedirectResponse(url=f"/web/admin-login.html?autoGoogle=1")
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "prompt": "consent",
        "access_type": "online",
        "state": base64.urlsafe_b64encode(next.encode()).decode(),
    }
    q = "&".join([f"{k}={httpx.QueryParams({k:v})[k]}" for k, v in params.items()])
    return RedirectResponse(url=f"https://accounts.google.com/o/oauth2/v2/auth?{q}")

@router.get("/google/callback")
def google_callback(code: str, state: str, db: Session = Depends(get_db)):
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=400, detail="Google OAuth not configured")
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    r = httpx.post("https://oauth2.googleapis.com/token", data=data, timeout=10)
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Token exchange failed")
    token_data = r.json()
    id_token = token_data.get("id_token")
    if not id_token:
        raise HTTPException(status_code=401, detail="No id_token")
    v = httpx.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": id_token}, timeout=10)
    if v.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid id_token")
    info = v.json()
    email = info.get("email")
    name = info.get("name") or f"{info.get('given_name','')} {info.get('family_name','')}".strip()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, hashed_password=get_password_hash("oauth"), full_name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
    jwt = create_access_token({"sub": str(user.id), "is_admin": user.is_admin})
    try:
        next = base64.urlsafe_b64decode(state).decode()
    except Exception:
        next = "/web/index.html"
    return RedirectResponse(url=f"{next}#token={jwt}")

@router.get("/config")
def auth_config():
    return {"google_client_id": settings.GOOGLE_CLIENT_ID}
