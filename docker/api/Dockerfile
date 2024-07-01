FROM ubuntu:22.04
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV ENV=dev
RUN apt-get update
RUN apt-get install -y build-essential python3-greenlet pip git wget
RUN pip install "poetry"
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN chmod +x docker/api/startup.sh
ENTRYPOINT docker/api/startup.sh