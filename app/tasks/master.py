from celery import Celery

from app.core import celery_config

app = Celery()

app.config_from_object(celery_config)
