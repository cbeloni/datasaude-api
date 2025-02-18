import asyncio
from core.utils.logger import LoggerUtils
import requests

from app.poluente.models import Poluente
from app.poluente.repository.poluente_repository import PoluenteRepository
from core.db import standalone_session

log = LoggerUtils(__name__)

async def execute_get_capa(persist: bool = False):

    @standalone_session
    async def salvar(p: Poluente):
        try:
            await PoluenteRepository().save(p)
        except Exception as e:
            # Registrar o erro em um log
            log.exception("Erro ao salvar: ", e)

    url = "https://arcgis.cetesb.sp.gov.br/server/rest/services/QUALAR/CETESB_QUALAR/MapServer/6/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry={%22xmin%22:-5244191.63658331,%22ymin%22:-2739503.0937498696,%22xmax%22:-5165920.11961926,%22ymax%22:-2661231.5767858177,%22spatialReference%22:{%22wkid%22:102100}}&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100"
    response = requests.get(url)
    data = response.json()
    poluentes = []
    for feature in data['features']:
        nome = feature['attributes']['Nome']
        data_split = feature['attributes']['DATA'].split(':')
        data = data_split[0] + ':' + data_split[1]
        situacao_rede = feature['attributes']['Situacao_Rede']
        qualidade = feature['attributes']['Qualidade'] or 'Não coletado'
        tipo_rede = feature['attributes']['Tipo_Rede']
        endereco = feature['attributes']['Endereco']
        indice = feature['attributes']['Indice']
        poluente_attri = feature['attributes']['POLUENTE']
        municipio = feature['attributes']['Municipio']

        poluente: Poluente = Poluente(nome=nome,
                                      situacao_rede=situacao_rede,
                                      tipo_rede=tipo_rede,
                                      data=data,
                                      qualidade=qualidade,
                                      endereco=endereco,
                                      indice=indice,
                                      poluente=poluente_attri,
                                      municipio=municipio)
        if persist:
            await salvar(poluente)
        poluentes.append(poluente)
    return poluentes