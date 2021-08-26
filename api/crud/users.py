from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security_utils import get_password_hash, verify_password
from models.dog import Dog
from models.user import User
from schemas.user import UserUpdate, UserCreate
from .dogs import get_dog_by_name


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> User:
    instance_user = db.query(User).filter(User.id == user_id).first()
    if instance_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return instance_user


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    instance_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
    )
    db.add(instance_user)
    db.commit()
    db.refresh(instance_user)
    return instance_user


def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    instance_user = get_user(db, user_id)
    if user.email:
        instance_user.email = user.email
    if user.full_name:
        instance_user.full_name = user.full_name
    if user.password:
        instance_user.password = get_password_hash(user.password)
    db.commit()
    db.refresh(instance_user)
    return instance_user


def delete_user(db: Session, user_id: int) -> User:
    instance_user = get_user(db, user_id)
    db.delete(instance_user)
    db.commit()
    return instance_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def adopt_dog(db: Session, user_id: int, dog_name: str) -> Dog:
    instance_dog = get_dog_by_name(db, dog_name)
    instance_dog.is_adopted = True
    instance_user = get_user(db, user_id)
    instance_user.dogs.append(instance_dog)
    db.commit()
    db.refresh(instance_dog)
    return instance_dog
