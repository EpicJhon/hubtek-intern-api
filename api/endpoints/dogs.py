from typing import List

from fastapi import APIRouter, BackgroundTasks

import crud.dogs as crud
from schemas.dog import Dog, DogUpdate
from .depends import *
from core.celery_app import celery_app

router = APIRouter()


class CommonDogParams:
    def __init__(self, dog_name: str, db: Session = Depends(get_db)):
        self.dog_name = dog_name
        self.db = db


class CommonDogParamsLogged(CommonDogParams):
    def __init__(self, dog_name: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
        super().__init__(dog_name, db)
        self.current_user = current_user


@router.get('/', response_model=List[Dog])
async def read_dogs(common: CommonPaginationParams = Depends(CommonPaginationParams)):
    return crud.get_dogs(common.db, common.skip, common.limit)


@router.get('/is_adopted', response_model=List[Dog])
async def read_dogs_adopted(common: CommonPaginationParams = Depends(CommonPaginationParams)):
    return crud.get_dogs_adopted(common.db, common.skip, common.limit)


@router.get('/{dog_name}', response_model=Dog)
async def read_dog(common: CommonDogParams = Depends(CommonDogParams)):
    return crud.get_dog_by_name(common.db, common.dog_name)


@router.post('/{dog_name}', response_model=Dog)
async def create_dog(background_task: BackgroundTasks, common: CommonDogParamsLogged = Depends(CommonDogParamsLogged)):
    def background_on_message(task):
        print(task.get(on_message=lambda m: print(m), propagate=False))

    instance_dog = await crud.create_dog(common.db, common.dog_name)

    # Send dog picture to guane API
    task = celery_app.send_task(
        'tasks.tasks.upload_file_from_url', args=[instance_dog.picture])
    print('tasks.tasks.upload_file_from_url', task)
    background_task.add_task(background_on_message, task)

    return instance_dog


@router.put('/{dog_name}', response_model=Dog)
async def update_dog(dog: DogUpdate, common: CommonDogParamsLogged = Depends(CommonDogParamsLogged)):
    return crud.update_dog(common.db, common.dog_name, dog)


@router.delete('/{dog_name}', response_model=Dog)
async def delete_dog(common: CommonDogParamsLogged = Depends(CommonDogParamsLogged)):
    return crud.delete_dog(common.db, common.dog_name)
