class PacienteCoordenadas:
    def __init__(self, id, id_paciente, endereco, latitude, longitude, x, y, acuracia, provider, response, data_criacao, data_alteracao):
        self.id = id
        self.id_paciente = id_paciente
        self.endereco = endereco
        self.latitude = latitude
        self.longitude = longitude
        self.x = x
        self.y = y
        self.acuracia = acuracia
        self.provider = provider
        self.response = response
        self.data_criacao = data_criacao
        self.data_alteracao = data_alteracao

    def __str__(self):
        return f"PacienteCoordenadas(id={self.id}, id_paciente={self.id_paciente}, endereco={self.endereco}, latitude={self.latitude}, longitude={self.longitude}, x={self.x}, y={self.y}, acuracia={self.acuracia}, provider={self.provider}, response={self.response}, data_criacao={self.data_criacao}, data_alteracao={self.data_alteracao})"