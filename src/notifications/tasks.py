import time
from src.shared.celery_app import celery_app

@celery_app.task
def send_welcome_email(email: str):
    time.sleep(5)
    print(f"EMAIL SENT TO {email}")
    return 