import os
from shapely.geometry import Point
import geopandas as gpd
from distutils import log
from core.db.session import session

PATH_VOLUME = os.environ.get('PATH_VOLUME')


def indice_poluente_por_utm(x, y, arquivo_geojson, campo):
    point_utm = Point(x, y)

    gdf = gpd.read_file(arquivo_geojson)
    result = gdf.contains(point_utm)

    if result.any():
        return gdf.loc[result, campo].values[0]

    log.error("O ponto UTM não está dentro do polígono.")
    return 0

def query_agrupado_data():
    return """
        SELECT count(1) qtd, DT_ATENDIMENTO
          FROM paciente
         WHERE dt_atendimento BETWEEN STR_TO_DATE(:dt_inicial, '%d%m%Y') AND STR_TO_DATE(:dt_final, '%d%m%Y')
      group by DT_ATENDIMENTO
      order by DT_ATENDIMENTO;
    """


def query_paciente_poluente():
    return """
        select p.ID, pc.id id_coordenada, replace(p.DT_ATENDIMENTO, '-','') dt_atendimento, pc.x, pc.y, pp.poluente, arquivo_geojson
          from paciente p,
               paciente_coordenadas pc,
               poluente_plot pp
         where p.ID = pc.id_paciente
           and replace(p.DT_ATENDIMENTO, '-','') =  pp.data_coleta
           and not exists (select 1 from paciente_interpolacao pi where pc.id = pi.id_coordenada and pp.poluente = pi.poluente)
           and pc.validado = 1
           and YEAR(STR_TO_DATE(p.DT_ATENDIMENTO, '%Y-%m-%d')) = :ano
           order by DT_ATENDIMENTO, p.id, pp.poluente asc
           limit :limit;
    """

def query_paciente_poluente_id():
    return """
        select p.ID, pc.id id_coordenada, replace(p.DT_ATENDIMENTO, '-','') dt_atendimento, pc.x, pc.y, pp.poluente, arquivo_geojson
          from paciente p,
               paciente_coordenadas pc,
               poluente_plot pp
         where p.ID = pc.id_paciente
           and replace(p.DT_ATENDIMENTO, '-','') =  pp.data_coleta
           and not exists (select 1 from paciente_interpolacao pi where pc.id = pi.id_coordenada and pp.poluente = pi.poluente)
           and pc.validado = 1
           and pc.id = :id
           order by DT_ATENDIMENTO, p.id, pp.poluente asc;
    """


def insert_paciente_interpolacao(id_coordenada, dt_atendimento, poluente, indice_interpolado):
    return """
        INSERT INTO paciente_interpolacao (id_coordenada, data, poluente, indice_interpolado)
        VALUES ('{}', '{}', '{}', '{}');
    """.format(str(id_coordenada), dt_atendimento, poluente, str(indice_interpolado))


async def indice_poluente_lote(pacienteInterpolacaoLote):
    log.info(f"Inicinado indice poluente lote: {pacienteInterpolacaoLote}")
    paciente_poluentes = (await session.execute(query_paciente_poluente(), pacienteInterpolacaoLote.to_dict())).all()
    indices_paciente_poluentes = []
    for row in paciente_poluentes:
        id, id_coordenada, dt_atendimento, x, y, poluente, arquivo_geojson = row
        indice_interpolado = indice_poluente_por_utm(x, y, PATH_VOLUME + arquivo_geojson, "media_diaria")
        query_paciente_interpolado = insert_paciente_interpolacao(id_coordenada, dt_atendimento, poluente, indice_interpolado)
        await session.execute(query_paciente_interpolado)
        await session.commit()
        dict_interpolado = {
            'id': id, 'id_coordenada': id_coordenada, 'dt_atendimento': dt_atendimento, 'x': x,
            'y': y, 'poluente': poluente, 'arquivo_geojson': arquivo_geojson, 'indice_interpolado': indice_interpolado,
        }
        indices_paciente_poluentes.append(dict_interpolado)
    return indices_paciente_poluentes

async def indice_poluente_por_id(pacienteInterpolacaoId):
    log.info(f"Inicinado indice poluente lote: {pacienteInterpolacaoId}")
    paciente_poluentes = (await session.execute(query_paciente_poluente_id(), pacienteInterpolacaoId.dict())).all()
    indices_paciente_poluentes = []
    for row in paciente_poluentes:
        id, id_coordenada, dt_atendimento, x, y, poluente, arquivo_geojson = row
        indice_interpolado = indice_poluente_por_utm(x, y, PATH_VOLUME + arquivo_geojson, "media_diaria")
        query_paciente_interpolado = insert_paciente_interpolacao(id_coordenada, dt_atendimento, poluente, indice_interpolado)
        await session.execute(query_paciente_interpolado)
        await session.commit()
        dict_interpolado = {
            'id': id, 'id_coordenada': id_coordenada, 'dt_atendimento': dt_atendimento, 'x': x,
            'y': y, 'poluente': poluente, 'arquivo_geojson': arquivo_geojson, 'indice_interpolado': indice_interpolado,
        }
        indices_paciente_poluentes.append(dict_interpolado)
    return indices_paciente_poluentes

async def consulta_agrupado_dt_atendimento(paciente_agrupado):
    log.info(f"Iniciado consulta agrupado: {paciente_agrupado}")
    pacientes_agrupados = (await session.execute(query_agrupado_data(), paciente_agrupado)).all()
    return pacientes_agrupados
