import requests, os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the CIDs.txt file
cids_file_path = os.path.join(current_dir, 'CIDs.txt')

# Read the CID values from the CIDs.txt file
with open(cids_file_path, 'r') as file:
    cids = file.read().splitlines()

# Set the URL and query parameters
url = 'https://datasaude-api.beloni.dev.br/api/v1/paciente/carga_previsao'
params = {
    'qtd_dias_corte': 2,
    'tipo_analise': 'INTERNACAO'
}

# Make the HTTP request for each CID value
for cid in cids:
    params['cid'] = cid
    response = requests.post(url, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        print(f'Request successful for CID: {cid}')
        print(response.json())
    else:
        # Request failed
        print(f'Request failed for CID: {cid}')
        print(response.text)
