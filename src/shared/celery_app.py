import os
from celery import Celery

BROKER_URL = os.getenv("BROKER_URL", "redis://localhost:6379/0")
RESULT_BACKEND = os.getenv("RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "taskflow",   # name of your celery app
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=["src.notifications.tasks"]  # where your tasks live
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)
