import logging
import os
from datetime import datetime
from elasticsearch import Elasticsearch
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import sys
import socket

load_dotenv()

ELASTIC_HOST = os.environ.get('ELASTIC_HOST')

class ElasticsearchHandler(logging.Handler):
    def __init__(self, hosts=None, index="logs"):
        super().__init__()
        self.es = Elasticsearch(hosts or ["http://localhost:9200"])
        self.index = index
        self.executor = ThreadPoolExecutor(max_workers=5)  # Define o número de threads
        self.hostname = socket.gethostname()  # Obter o hostname da máquina

    def emit(self, record):
        log_entry = self.format(record)
        log_document = {
            "timestamp": datetime.now(),
            "level": record.levelname,
            "message": log_entry,
            "logger_name": record.name,
            "module": record.module,
            "func_name": record.funcName,
            "line": record.lineno,
            "app": "datasaude-api",
            "hostname": self.hostname  # Adicionar o hostname ao documento de log
        }
        # Envia o log para o Elasticsearch de forma assíncrona
        self.executor.submit(self.send_log, log_document)

    def send_log(self, log_document):
        self.es.index(index=self.index, body=log_document)

class LoggerUtils:
    def __init__(self, name=__name__, log_file='app.log', es_index='logs', es_hosts=ELASTIC_HOST):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Definir o formato do log
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Configurar o manipulador de arquivo rotativo para o logger
        file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=10)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Configura o Handler para enviar logs para o Elasticsearch
        es_handler = ElasticsearchHandler(hosts=es_hosts, index=es_index)
        es_formatter = logging.Formatter("%(message)s")
        es_handler.setFormatter(es_formatter)
        self.logger.addHandler(es_handler)

        # Configurar o manipulador de stream para o stdout
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger

    def __getattr__(self, name):
        return getattr(self.logger, name)