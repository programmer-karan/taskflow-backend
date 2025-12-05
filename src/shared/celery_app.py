import os
from celery import Celery

# 1. Get the URL from the environment
# Docker sets REDIS_URL=redis://redis:6379/0
# We default to localhost ONLY if the env var is missing (for local testing)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "taskflow",
    broker=REDIS_URL,   # <--- Use the variable!
    backend=REDIS_URL,  # <--- Use the variable!
    include=["src.notifications.tasks"]
)

# 2. Ensure configuration updates apply
celery_app.conf.update(
    broker_url=REDIS_URL,
    result_backend=REDIS_URL,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
