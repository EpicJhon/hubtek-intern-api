from typing import List

from fastapi import APIRouter

import crud.users as crud
from schemas.dog import Dog
from schemas.user import User, UserCreate, UserUpdate
from .depends import *

router = APIRouter()


class CommonUserParams:
    def __init__(self, user_id: int, db: Session = Depends(get_db)):
        self.user_id = user_id
        self.db = db


class CommonUserParamsLogged(CommonUserParams):
    def __init__(self, user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
        super().__init__(user_id, db)
        self.current_user = current_user


@router.get('/', response_model=List[User])
async def read_users(common: CommonPaginationParams = Depends(CommonPaginationParams)):
    return crud.get_users(common.db, common.skip, common.limit)


@router.get('/{user_id}', response_model=User)
async def read_user(common: CommonUserParams = Depends(CommonUserParams)):
    return crud.get_user(common.db, common.user_id)


@router.post('/', response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_user(db, user)


@router.put('/{user_id}', response_model=User)
async def update_user(user: UserUpdate, common: CommonUserParamsLogged = Depends(CommonUserParamsLogged)):
    return crud.update_user(common.db, common.user_id, user)


@router.delete('/{user_id}', response_model=User)
async def delete_user(common: CommonUserParamsLogged = Depends(CommonUserParamsLogged)):
    return crud.delete_user(common.db, common.user_id)


@router.put('/adopt/{user_id}/{dog_name}', response_model=Dog)
async def adopt_dog(user_id: int, dog_name: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.adopt_dog(db, user_id, dog_name)
