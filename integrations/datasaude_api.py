import os, requests
import logging
from dotenv import load_dotenv

load_dotenv()

_datasaude_api = os.environ.get('DATASAUDE_API')

log = logging.getLogger(__name__)


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
        log.error(f"Erro ao enviar paciente_salvar: {e}")
        raise Exception("Erro ao enviar paciente_salvar", e)
