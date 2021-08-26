import uvicorn
from fastapi import FastAPI, APIRouter

import crud
import endpoints
from core import settings, engine, Base, SessionLocal
from schemas.user import UserCreate

# Populate database for first use time
Base.metadata.create_all(bind=engine)
db = SessionLocal()
user = crud.users.get_user_by_email(db, email=settings.FIRST_USER)
if not user:
    instance_user = UserCreate(
        email=settings.FIRST_USER,
        password=settings.FIRST_USER_PWD,
    )
    user = crud.users.create_user(db, instance_user)

# Configure FastAPI
app = FastAPI()

api_router = APIRouter()

api_router.include_router(endpoints.login.router, tags=['login'])
api_router.include_router(endpoints.dogs.router, prefix='/dogs', tags=['dogs'])
api_router.include_router(endpoints.users.router, prefix="/users", tags=['users'])

app.include_router(api_router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9050)
