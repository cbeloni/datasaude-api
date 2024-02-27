import logging
import os
import click
import uvicorn
from logging.handlers import RotatingFileHandler
from core.config import config
from app.server import app
from fastapi.middleware.cors import CORSMiddleware

# Configurar o logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Definir o formato do log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Configurar o manipulador de arquivo rotativo para o logger
file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=10)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Redirecionar a saída padrão (stdout) para o logger
# sys.stdout = open('stdout.log', 'w')
# sys.stderr = open('stderr.log', 'w')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "dev", "prod"], case_sensitive=False),
    default="local",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)
def main(env: str, debug: bool):
    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)
    uvicorn.run(
        app="app.server:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.ENV != "production" else False,
        workers=1,
    )


if __name__ == "__main__":
    main()
