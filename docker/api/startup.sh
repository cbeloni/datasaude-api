#!/bin/bash
dockerize -wait tcp://db:3306 -timeout 120s
#alembic upgrade head && gunicorn --bind 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker app.server:app --log-file=datasaude.log --log-level=debug
gunicorn --bind 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker app.server:app --log-file=datasaude.log --log-level=debug