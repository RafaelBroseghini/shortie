# shortie
> A FastAPI + Redis URL Shortener :)

## Redis
> ...

## Celery
*  `celery upgrade settings app/core/celery_config.py`
*  `celery -A app.tasks.master worker -l INFO`