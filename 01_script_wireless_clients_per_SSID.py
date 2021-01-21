"""
    Importação de módulos python.
    A codificação do arquivo deve estar em UTF-8.
"""
import requests
import json
import sys

from prtg.sensor.result import CustomSensorResult
from prtg.sensor.units import ValueUnit

"""
    Parâmetros de Autenticação de API no Dashboard Meraki.
    A API-Key deve ser setada dentro do Dashboard Meraki ou utilizar uma API-Key pública para testes.
"""
payload_meraki = {}
headers_meraki = {
    'X-Cisco-Meraki-API-Key': 'COLOQUE AQUI A SUA API KEY'
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

"""
    URL para consulta na API Meraki.
    A consulta API está documentada em: https://developer.cisco.com/meraki/api/#!get-network-clients
    Operation Id: getNetworkClients
    A URL consulta a lista total de clientes para uma NETWORK específica dentro do intervalo de tempo parametrizado.
    O intervalo de tempo está configurado para 7200 segundos (2 horas)
    Para não lidar com paginação é feita a extração de 1000 registros por página. 
"""
url_clients = 'https://api.meraki.com/api/v0/networks/%s/clients?timespan=7200&perPage=1000' % my_network

if __name__ == "__main__":
    try:
        
        # Consulta da API        
        meraki_clients = requests.request("GET", url_clients, headers=headers_meraki, data=payload_meraki)
        my_clients = json.loads(meraki_clients.text)
    
        # Criação de lista para a contagem.
        my_ssid_clients = []

        # Os resultados da consulta API são filtrados para clientes online e associados em um SSID específico.
        for indice_clients in my_clients:
            if indice_clients["status"] == "Online" and indice_clients["ssid"] == "COLOQUE_SEU_SSID":
                my_ssid_clients.append(indice_clients["id"])
            
        # Criação do Canal Primário dentro do Sensor PRTG 
        data = json.loads(sys.argv[1])
        csr = CustomSensorResult(text="This sensor runs on %s" % data["host"])
        csr.add_primary_channel(name="My SSID Clients",
                                value=len(my_ssid_clients),
                                unit=ValueUnit.COUNT,
                                is_float=False)
        print(csr.json_result)  
    except Exception as e:
        csr = CustomSensorResult(text="Python Script execution error")
        csr.error = "Python Script execution error: %s" % str(e)
        print(csr.json_result)