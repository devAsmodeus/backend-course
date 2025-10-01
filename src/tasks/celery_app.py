from celery import Celery

from src.config import settings


celery_instance = Celery(
    'tasks',
    broker=settings.redis_url,
    include=[
        'src.tasks.tasks',
    ],
    # result_backend=settings.redis_url
)