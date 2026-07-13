import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()


celery_app = Celery("mindbot")

celery_app.conf.broker_url = os.getenv("REDIS_LINK", "redis://localhost:6379/0")
celery_app.conf.result_backend = os.getenv("REDIS_LINK", "redis://localhost:6379/0")


celery_app.conf.imports = ("app.workers.tasks",)

