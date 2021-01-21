"""
    Importação de módulos python.
    A codificação do arquivo deve estar em UTF-8.
"""
import requests
import json
import sys

"""
    Parâmetros de Autenticação de API no Dashboard Meraki.
    A API-Key deve ser setada dentro do Dashboard Meraki ou utilizar uma API-Key pública para testes.
"""
payload_meraki = {}
headers_meraki = {
    'X-Cisco-Meraki-API-Key': '3ac54d2d8a4ddff80ece8ebd2ff3ecc12aaad08f'
}

"""
    Definição de variáveis para a consulta via API.
    As variáveis podem ser configuradas de forma estática ou dinâmica.
"""
# Código da Organization
my_org = "COLOQUE AQUI O CÓDIGO DE SUA ORGANIZATION"

# Código da Network.
my_network = "COLOQUE AQUI O CÓDIGO DE SUA NETWORK"

# Serial do Device
my_serial = "COLOQUE AQUI O CÓDIGO SERIAL DO DISPOSITIVO"

# URL para consulta na API Meraki.
url_clients = 'https://api.meraki.com/api/v0/networks/%s/clients?timespan=7200&perPage=1000' % my_network

"""
    URL para consulta na API Meraki.
    A consulta API está documentada em: https://developer.cisco.com/meraki/api/#!get-network-clients
    Operation Id:getNetworkClients
    A URL consulta a lista total de clientes para uma NETWORK específica dentro do intervalo de tempo parametrizado.
    O intervalo de tempo está configurado para 7200 segundos (2 horas)
    Para não lidar com paginação é feita a extração de 1000 registros por página. 
"""
meraki_clients = requests.request("GET", url_clients, headers=headers_meraki, data = payload_meraki)
my_clients = json.loads(meraki_clients.text)

"""
    Testes para visualizar e manipular os dados.
    No caso da paginação de dados é necessário alterar o script.
"""
# Criação de uma lista para a contagem do total de clientes.
my_ssid_clients = []

# Imprime o conteúdo original da consulta da API Meraki.
print(json.dumps(my_clients, indent=4))

# Imprime o tipo de dados python gerado pela consulta da API Meraki.
print("\n")
print(type(my_clients))

"""
    Realizar uma iteração na lista extraída da consulta API Meraki.
    Filtra os resultados que tiverem o SSID solicitado e serem clientes Online.
    Carrega os resultados filtrados dentro de uma nova lista.
"""
for indice_clients in my_clients:
    if indice_clients["ssid"] == "COLOQUE SEU SSID" and indice_clients["status"] == "Online":
        my_ssid_clients.append(indice_clients["id"])

# Imprime o total de clientes conectados do SSID solicitado.
print("My SSID Connected Clients: ", len(my_ssid_clients))

