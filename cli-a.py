import json
import requests

# Crea el JSON que deseas enviar en el cuerpo de la petición
data = {"archivo": 'reut2-004.sgm'}

# Crea la petición POST
response = requests.post("http://127.0.0.1:8090/a-num_palabras", json=data)

# Verifica el estado de la respuesta
if response.status_code == 200:
	json_response = response.json()
	print(json_response)
	print("Petición exitosa")
else:
    print(f"Error: {response.status_code}")



# Crea la petición POST
response = requests.post("http://127.0.0.1:8090/b-freq_palabras", json=data)

# Verifica el estado de la respuesta
if response.status_code == 200:
	json_response = response.json()
	print(json_response)
	print("Petición exitosa")
else:
    print(f"Error: {response.status_code}")