import os, requests
from core.utils.logger import LoggerUtils
from dotenv import load_dotenv

load_dotenv()

_datasaude_api = os.environ.get('DATASAUDE_API')

log = LoggerUtils(__name__)


async def paciente_salvar(payload):
    try:
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", f"{_datasaude_api}/paciente/salvar", headers=headers, data=payload)
        return response
    except Exception as e:
        log.error(f"Erro ao enviar paciente_salvar: {e}")
        raise Exception("Erro ao enviar paciente_salvar", e)


async def geolocalizacao_salvar(id: int):
    try:
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", f"{_datasaude_api}/paciente/coordenadas/{id}", headers=headers)
        return response
    except Exception as e:
        log.error(f"Erro ao enviar geolocalizacao_salvar: {e}")
        raise Exception("Erro ao enviar geolocalizacao_salvar", e)

async def interpolacao_salvar(id: int):
    try:
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", f"{_datasaude_api}/paciente/interpolacao/{id}", headers=headers)
        return response
    except Exception as e:
        log.error(f"Erro ao enviar interpolacao_salvar: {e}")
        raise Exception("Erro ao enviar interpolacao_salvar", e)
