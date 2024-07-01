FROM ubuntu:22.04
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .
RUN apt-get update
RUN apt-get install -y build-essential python3-greenlet pip git wget
RUN pip install "poetry"
RUN poetry config virtualenvs.create false
RUN poetry lock --no-update
RUN poetry install --no-dev
RUN chmod +x startup.sh
ENTRYPOINT startup.sh