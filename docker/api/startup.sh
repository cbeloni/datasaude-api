#!/bin/bash
dockerize -wait tcp://db:3306 -timeout 120s
python3 listeners/paciente_listener.py > paciente_listener.log &
python3 listeners/geolocalizacao_listener.py > geolocalizacao_listener.log &
alembic upgrade head && gunicorn --bind 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker app.server:app --log-file=datasaude.log --log-level=debug