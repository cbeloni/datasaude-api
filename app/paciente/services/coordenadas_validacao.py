import os
from shapely.geometry import Point
import geopandas as gpd

PATH_VOLUME = os.environ.get('PATH_VOLUME')

_retorno = {}

def tem_localizacao_contorno_valida(x, y):
    point_utm = Point(x, y)

    gdf = gpd.read_file(PATH_VOLUME + "geojson/RMSP_CONTORNO.geojson")
    result = gdf.contains(point_utm)
    return result.any()

def validacao_openstreetmap(coordenadas):
    if int(coordenadas['acuracia']) < 26:
        _retorno['validado'] = 0
        _retorno['response'] = 'Acurácia abaixo de 26'
        return _retorno

    if not tem_localizacao_contorno_valida(coordenadas['x'], coordenadas['y']):
        _retorno['validado'] = -1
        _retorno['response'] = 'Localização fora da grande SP'
        return _retorno

    return _retorno


def validacao_opencage(coordenadas):
    if int(coordenadas['acuracia']) < 8:
        _retorno['validado'] = 0
        _retorno['response'] = 'Acurácia abaixo de 8'
        return _retorno
    if coordenadas['country'] != 'Brazil':
        _retorno['validado'] = 0
        _retorno['response'] = 'country não é Brazil'
        return _retorno
    if not tem_localizacao_contorno_valida(coordenadas['x'], coordenadas['y']):
        _retorno['validado'] = -1
        _retorno['response'] = 'Localização fora da grande SP'
        return _retorno
    return _retorno


def validacao_googlemaps(coordenadas):
    if coordenadas['acuracia'] not in ('ROOFTOP', 'RANGE_INTERPOLATED'):
        _retorno['validado'] = 0
        _retorno['response'] = "Acurácia diferente de ROOFTOP e RANGE_INTERPOLATED"
        return _retorno
    return _retorno


_validacoes = {
    'openstreetmap': validacao_openstreetmap,
    'googlemaps': validacao_googlemaps,
    'opencage': validacao_opencage,
}


def validacao(provider, coordenadas):
    _retorno['validado'] = 1
    _retorno['response'] = coordenadas['response']
    validacao_impl = _validacoes[provider]
    return validacao_impl(coordenadas)


if __name__ == '__main__':
    opencage_valido = {'acuracia': 8, 'country': 'BRAZIL', 'county': 'Região Metropolitana de São Paulo'}
    valid = validacao('opencage', opencage_valido)
    print(f"opencage valido: {valid}")

    opencage_invalido = {'acuracia': 7, 'country': 'BRAZIL', 'county': 'Região Metropolitana de São Paulo'}
    valid = validacao('opencage', opencage_invalido)
    print(f"opencage invalido: {valid}")