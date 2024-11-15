import requests

def obtener_nombres_de_paises():
    """
    Obtiene los nombres de todos los países, ordenados alfabéticamente.
    """
    # URL del endpoint para obtener todos los países
    url = "https://restcountries.com/v3.1/all"

    # Hacer la solicitud GET
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        countries = response.json()  # Convertir la respuesta en formato JSON
        
        # Extraer solo los nombres comunes de los países
        country_names = [country['name']['common'] for country in countries]
        
        # Ordenar alfabéticamente los nombres de los países
        country_names_sorted = sorted(country_names)
        
        return country_names_sorted
    else:
        print("Error al obtener los países")
        return []
