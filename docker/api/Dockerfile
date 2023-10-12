FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /home
WORKDIR /home
ENV ENV=dev
RUN apt-get update -y && \
    apt-get install -y python3-rtree python3-geopandas
RUN pip install "poetry>=1.3.0,<1.4.0"
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN chmod +x /home/docker/api/startup.sh
ENTRYPOINT /home/docker/api/startup.sh