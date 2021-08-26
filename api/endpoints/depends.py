from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

import models
import schemas
from core import security
from core.config import settings
from core.database import SessionLocal
import crud


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl='/api/login/access-token'
)


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.users.get_user(db, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


class CommonPaginationParams:
    def __init__(self, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        self.skip = skip
        self.limit = limit
        self.db = db
