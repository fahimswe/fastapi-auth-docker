from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from .models import User
from .database import engine
from argon2 import PasswordHasher
from jose import jwt
import time

router = APIRouter()
ph = PasswordHasher()
SECRET_KEY = "SUPERSECRET123"
ALGO = "HS256"

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == form_data.username)).first()

        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        try:
            ph.verify(user.password_hash, form_data.password)
        except:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        token = jwt.encode(
            {"sub": user.email, "exp": time.time() + 3600},
            SECRET_KEY,
            algorithm=ALGO
        )

        return {"access_token": token, "token_type": "bearer"}
