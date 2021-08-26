from celery import Celery
from .config import settings

celery_app = Celery(
    'tasks',
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND
)
