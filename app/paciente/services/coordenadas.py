import os
import requests
import pyproj
import logging
from geopy.geocoders import Nominatim

from api.paciente.v1.response.paciente_coordenadas_response import CoordenadasResponse

open_cage_api_key = os.environ.get('OPEN_CAGE_API_KEY')
google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')

log = logging.getLogger(__name__)

def execute(address, provider):

    try:
        response  = {}
        if provider == 'opencage':
            latitude, longitude, acuracia, json_data, components = get_latitude_longitude_opencage(address)
            x, y = converte_coordenadas_UTM(latitude, longitude)
            response = {"latitude": latitude, "longitude": longitude, "acuracia": acuracia, "x": x, "y": y,
                        "response": str(json_data)}
            response.update(components)
        if provider == 'googlemaps':
            latitude, longitude, acuracia, json_data, components = get_latitude_longitude_gmaps(address)
            x, y = converte_coordenadas_UTM(latitude, longitude)
            response = {"latitude": latitude, "longitude": longitude, "acuracia": acuracia, "x": x, "y": y,
                        "response": str(json_data)}
            response.update(components)
        if provider == 'openstreetmap':
            latitude, longitude, acuracia, x, y = get_free_coordenadas_utm_do_endereco(address)
            response = {"latitude": latitude, "longitude": longitude, "acuracia": acuracia, "x": x, "y": y,
                        "response": '{}', "components": '{}'}
        return response
    except Exception as e:
        log.error("Erro ao obter coordenada", exc_info=True)


    return {"latitude": '', "longitude": '', "acuracia": '', "x": '', "y": '', "response": '{}'}

def get_latitude_longitude_opencage(address):
    log.info('start opencage: ' + address + " key: " + open_cage_api_key)
    url = "https://api.opencagedata.com/geocode/v1/json?key=%s&q=%s" % (open_cage_api_key, address)
    response = requests.get(url)
    log.info('response opencage: ' + address + " key: " + open_cage_api_key)
    json_data = response.json()
    results = json_data['results']
    latitude = results[0]['geometry']['lat']
    longitude = results[0]['geometry']['lng']
    confidence = results[0]['confidence']
    components = results[0]['components']
    components['formatted'] = results[0]['formatted']
    return (latitude, longitude, confidence, json_data, components)


def converte_coordenadas_UTM(latitude, longitude):
    input_crs = pyproj.CRS.from_epsg(4326)
    output_crs = pyproj.CRS.from_epsg(29193)

    transformer = pyproj.Transformer.from_crs(input_crs, output_crs, always_xy=True)

    # Converta de latitude e longitude para UTM
    return transformer.transform(longitude, latitude)


def get_free_coordenadas_utm_do_endereco(endereco):
    try:
        # Inicialize o geocoder
        geolocator = Nominatim(user_agent="myGeocoder")

        # Obtenha as coordenadas geográficas (latitude e longitude) do endereço
        location = geolocator.geocode(endereco)

        if location:
            latitude = location.latitude
            longitude = location.longitude
            place_rank = location.raw["place_rank"]

            # Defina a projeção de coordenadas para UTM 29T (código 29193)
            utm = pyproj.Proj("+proj=utm +zone=23 +south +ellps=aust_SA + towgs84")

            # Converta as coordenadas geográficas em coordenadas UTM
            utm_x, utm_y = utm(longitude, latitude)

            return latitude, longitude, place_rank, utm_x, utm_y
        else:
            raise {"Endereço não encontrado ou geocodificação falhou."}
    except Exception as e:
        raise {"error": str(e)}


def get_latitude_longitude_gmaps(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (address, google_maps_api_key)
    response = requests.get(url)
    json_data = response.json()
    results = json_data['results']
    location = results[0]['geometry']['location']
    location_type = results[0]['geometry']['location_type']
    components = {}
    for component in results[0]["address_components"]:
        if "route" in component["types"]:
            components['formatted'] = component["long_name"]
        if "postal_code" in component["types"]:
            components['postcode'] = component["long_name"]
        if "sublocality" in component["types"]:
            components['quarter'] = component["long_name"]
        if "administrative_area_level_4" in component["types"]:
            components['suburb'] = component["long_name"]
        if "administrative_area_level_2" in component["types"]:
            components['city'] = component["long_name"]
        if "administrative_area_level_1" in component["types"]:
            components['state'] = component["long_name"]
        if "country" in component["types"]:
            components['country'] = component["long_name"]


    latitude = location['lat']
    longitude = location['lng']
    return latitude, longitude, location_type, json_data, components
