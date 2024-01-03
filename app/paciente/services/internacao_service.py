import requests
import json, os

from api.paciente.v1.request.paciente_internacao import PacienteInternacaoPayload

datasaude_ml_url = os.environ.get('DATASAUDE_ML_URL')

def execute(pacienteInternacaoPayload: PacienteInternacaoPayload, token):
    url = datasaude_ml_url
    payload = json.dumps(pacienteInternacaoPayload.dict())
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


if __name__ == '__main__':
    json_data = {
        "Inputs": {
            "data": [
                {
                    "MP10_NORMALIZADO": 0.106,
                    "O3_NORMALIZADO": 0.356,
                    "TEMP_NORMALIZADO": 0.625,
                    "UR_NORMALIZADO": 0.649,
                    "DS_CID_GRAVIDADE": "OUTROS TRANSTORNOS RESPIRATORIOS",
                    "outono": 0,
                    "inverno": 0,
                    "primavera": 0,
                    "verao": 1,
                    "Jan": 0,
                    "Feb": 1,
                    "Mar": 0,
                    "Apr": 0,
                    "May": 0,
                    "Jun": 0,
                    "Jul": 0,
                    "Aug": 0,
                    "Sep": 0,
                    "Oct": 0,
                    "Nov": 0,
                    "Dec": 0,
                    "MENOR_1_ANO": "0",
                    "ENTRE_1_4_ANOS": "1",
                    "ENTRE_5_9_ANOS": "0",
                    "ENTRE_10_14_ANOS": "0",
                    "ENTRE_15_18_ANOS": "0",
                    "TP_SEXO": "F"
                }
            ]
        }
    }

    input_payload = PacienteInternacaoPayload(**json_data)
    response = execute(input_payload)
    print(response.text)
