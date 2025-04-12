import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config.database import get_db
from models.user import User
from services.user_service import get_user_by_username_service, verify_password

login_router = APIRouter()

SECRET_KEY = os.environ.get("SECRET_KEY", "secretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/")


class LoginSchema(BaseModel):
    username: str
    password: str


def create_access_token(data: dict, expires_delta: float = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid token payload"
            )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_username_service(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@login_router.post("/")
def login(form_data: LoginSchema, db: Session = Depends(get_db)):
    user = get_user_by_username_service(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
