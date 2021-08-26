from core.celery_app import celery_app
from celery import current_task
from time import sleep
import requests
import os


@celery_app.task
def test_celery(word: str) -> str:
    for i in range(1, 11):
        sleep(1)
        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': i * 10})
    return f"test task return {word}"


@celery_app.task
def upload_file_from_url(url: str) -> str:
    file = requests.get(url).content

    api_url = 'https://gttb.guane.dev/api/files'
    response = requests.post(api_url, files={'file': (os.path.basename(url), file)})
    return response.json().get('filename')
