from datetime import datetime
from typing import Optional

from pydantic import HttpUrl, BaseModel, Field


class DogBase(BaseModel):
    name: str
    picture: Optional[HttpUrl] = None
    is_adopted: Optional[bool] = None


class Dog(DogBase):
    id: int
    create_date: datetime
    user_id: Optional[int] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                'id': 1,
                'name': 'Lazy',
                'picture': 'https://images.dog.ceo/breeds/papillon/n02086910_6483.jpg',
                "create_date": '2020-02-20 20:58:55.164954',
                "is_adopted": True,
            }
        }


class DogUpdate(DogBase):
    pass
