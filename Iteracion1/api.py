import requests
# Importamos la librería ctypes
import ctypes


# Cargamos la libreria 
libApi = ctypes.CDLL('./libApi.so')

# Definimos los tipos de los argumentos de la función procesarNumero
libApi.procesarNumero.argtypes = (ctypes.c_float,)

# Definimos el tipo del retorno de la función procesarNumero
libApi.procesarNumero.restype = ctypes.c_int

# URL de la API
url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI"
params = {
    "format": "json",
    "date": "2011:2020",
    "per_page": 32500,
    "page": 1,
    "country": "Argentina"
}

# Solicitar al usuario el nombre del país y la fecha
country_name = input("Ingrese el nombre del país: ")
target_date = input("Ingrese el año (formato YYYY): ")

# Realizar la solicitud GET
response = requests.get(url, params=params)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()
    
    # Extraer el bloque de datos (segundo elemento del JSON)
    records = data[1] if len(data) > 1 else []
    
    # Buscar el valor de un país y fecha específicos
    value_found = None

    for record in records:
        country = record.get("country", {}).get("value")
        date = record.get("date")
        value = record.get("value")
        
        if country == country_name and date == target_date:
            value_found = value
            break

    # Mostrar el resultado
    if value_found is not None:
        print(f"El valor de Gini para {country_name} en {target_date} es: {value_found}")
        # Llamar a C
        print("Llamando a la función procesarNumero de C: " + str(libApi.procesarNumero(value_found)))# Llamamos a la función procesarNumero
    else:
        print(f"No se encontró información para {country_name} en {target_date}.")
else:
    print(f"Error en la solicitud: {response.status_code}")
