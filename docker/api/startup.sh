#!/bin/bash
dockerize -wait tcp://db:3306 -timeout 120s
celery -A celery_task worker --loglevel=info & > celery.log &
celery -A celery_task flower --port=5001 & > celery_flower.log &
alembic upgrade head && gunicorn --bind 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker app.server:app --log-file=datasaude.log --log-level=debug