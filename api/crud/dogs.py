from typing import List

import requests
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import true

from models.dog import Dog
from schemas.dog import DogUpdate


async def get_dog_picture():
    url = 'https://dog.ceo/api/breeds/image/random'
    response = requests.get(url)
    return response.json().get('message')


def get_dogs(db: Session, skip: int = 0, limit: int = 100) -> List[Dog]:
    return db.query(Dog).offset(skip).limit(limit).all()


def get_dogs_adopted(db: Session, skip: int = 0, limit: int = 100) -> List[Dog]:
    return db.query(Dog).filter(Dog.is_adopted == true()).offset(skip).limit(limit).all()  # noqa


def get_dog_by_name(db: Session, dog_name: str) -> Dog:
    instance_dog = db.query(Dog).filter(Dog.name == dog_name).first()
    if instance_dog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Dog not found')
    return instance_dog


async def create_dog(db: Session, dog_name: str, ) -> Dog:
    instance_dog = Dog(
        name=dog_name,
        picture=await get_dog_picture()
    )
    db.add(instance_dog)
    db.commit()
    db.refresh(instance_dog)
    return instance_dog


def update_dog(db: Session, dog_name: str, dog: DogUpdate) -> Dog:
    instance_dog = get_dog_by_name(db, dog_name)
    instance_dog.name = dog.name
    instance_dog.is_adopted = dog.is_adopted
    db.commit()
    db.refresh(instance_dog)
    return instance_dog


def delete_dog(db: Session, dog_name: str) -> Dog:
    instance_dog = get_dog_by_name(db, dog_name)
    db.delete(instance_dog)
    db.commit()
    return instance_dog
