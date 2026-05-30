FROM ubuntu:22.04
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instale os pacotes do sistema de forma otimizada e limpe o cache do apt
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
    python3-greenlet \
    python3-pip \
    git \
    wget \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Instale e configure o poetry antes de copiar os arquivos fonte
RUN pip install "poetry" \
    && poetry config virtualenvs.create false

# Copie apenas arquivos de configuração de dependência do Poetry
COPY pyproject.toml poetry.lock ./

# Use cache do BuildKit para instalação rápida das dependências python (sem reinstalar toda vez)
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/pypoetry \
    poetry install --no-root --no-interaction --no-ansi

# Copie o restante do código fonte
COPY . .

# ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.server:app"]
ENTRYPOINT ["python3","main.py"]
