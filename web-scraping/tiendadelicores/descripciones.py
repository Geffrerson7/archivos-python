import requests
from bs4 import BeautifulSoup
import pandas as pd

# Leer el archivo Excel con las URLs
excel_file = "C:/Users/geffe/Documents/SILABUZ/tiendadelicorescom/links-descripciones.xlsx"  # Cambia esto al nombre de tu archivo Excel
df = pd.read_excel(excel_file)

# Lista para almacenar las descripciones
descripciones_total = []

# Iterar sobre las URLs en el archivo Excel
for url in df['URL']:
    # Realizar la solicitud HTTP
    response = requests.get(url)
    if response.status_code == 200:
        # Parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todos los párrafos con la clase 'text-base text-gray-900'
        descripciones = soup.find_all('p', class_='text-base text-gray-900')

        # Agregar las descripciones a la lista
        descripciones_total.append('\n'.join([descripcion.text for descripcion in descripciones]))
        
    elif response.status_code == 403:
        print(f"Error: Forbidden (403) al acceder a la URL: {url}")
    else:
        print(f"Error: {response.status_code} al acceder a la URL: {url}")

# Agregar las descripciones a un DataFrame
df['Descripciones'] = descripciones_total

# Guardar el DataFrame en un nuevo archivo Excel
excel_output = "C:/Users/geffe/Documents/SILABUZ/tiendadelicorescom/descripciones.xlsx"  # Nombre del archivo de salida
df.to_excel(excel_output, index=False)

print("Descripciones guardadas en el archivo:", excel_output)
