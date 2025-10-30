from celery import Celery

from src.config import settings


celery_instance = Celery(
    "tasks",
    broker=settings.redis_url,
    include=[
        "src.tasks.tasks",
    ],
    # result_backend=settings.redis_url
)

celery_instance.conf.beat_schedule = {
    "The first": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}
