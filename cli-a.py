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

data2 = {"topn":2}
# Crea la petición POST
response = requests.post("http://127.0.0.1:8090/c-max_freq_palabras", json=data2)

# Verifica el estado de la respuesta
if response.status_code == 200:
	json_response = response.json()
	print(json_response)
	print("Petición exitosa")
else:
    print(f"Error: {response.status_code}")


data3 = {"archivo": 'reut2-004.sgm',"topn":2}
# Crea la petición POST
response = requests.post("http://127.0.0.1:8090/d-max_freq_palabras", json=data3)

# Verifica el estado de la respuesta
if response.status_code == 200:
	json_response = response.json()
	print(json_response)
	print("Petición exitosa")
else:
    print(f"Error: {response.status_code}")



data3 = {"archivo": 'reut2-004.sgm|reut2-001.sgm',"topn":2}
# Crea la petición POST
response = requests.post("http://127.0.0.1:8090/d-max_freq_palabras", json=data3)

# Verifica el estado de la respuesta
if response.status_code == 200:
	json_response = response.json()
	print(json_response)
	print("Petición exitosa")
else:
    print(f"Error: {response.status_code}")



data4 = {"listaarchivos": 'reut2-004.sgm|reut2-001.sgm',"topn":2,"flagsinrank":0}
# Crea la petición POST
response = requests.post("http://127.0.0.1:8090/e-dos_max_freq_palabras", json=data4)

# Verifica el estado de la respuesta
if response.status_code == 200:
	json_response = response.json()
	print(json_response)
	print("Petición exitosa")
else:
    print(f"Error: {response.status_code}")
ata5 = {"listaarchivos": 'reut2-004.sgm|reut2-001.sgm|reut2-002.sgm|reut2-003.sgm',"topn":2,"flagsinrank":0}
 Crea la petición POST
response = requests.post("http://127.0.0.1:8090/f-n_max_freq_palabras", json=data5)

# Verifica el estado de la respuesta
if response.status_code == 200:
	json_response = response.json()
	print(json_response)
	print("Petición exitosa")
else:
    print(f"Error: {response.status_code}")