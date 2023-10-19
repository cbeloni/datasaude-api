def validacao_openstreetmap(coordenadas):
    if int(coordenadas['acuracia']) < 26:
        return False
    return True


def validacao_opencage(coordenadas):
    if int(coordenadas['acuracia']) < 8:
        return False
    if coordenadas['country'] != 'BRAZIL':
        return False
    if coordenadas['county'] not in ('São Paulo', 'Região Metropolitana de São Paulo'):
        return False
    return True


def validacao_googlemaps(coordenadas):
    if coordenadas['acuracia'] not in ('ROOFTOP', 'RANGE_INTERPOLATED'):
        return False
    return True


_validacoes = {
    'openstreetmap': validacao_openstreetmap,
    'googlemaps': validacao_googlemaps,
    'opencage': validacao_opencage,
}


def validacao(provider, coordenadas):
    validacao = _validacoes[provider]
    return {'validado':  validacao(coordenadas)}


if __name__ == '__main__':
    opencage_valido = {'acuracia': 8, 'country': 'BRAZIL', 'county': 'Região Metropolitana de São Paulo'}
    valid = validacao('opencage', opencage_valido)
    print(f"opencage valido: {valid}")

    opencage_invalido = {'acuracia': 7, 'country': 'BRAZIL', 'county': 'Região Metropolitana de São Paulo'}
    valid = validacao('opencage', opencage_invalido)
    print(f"opencage invalido: {valid}")