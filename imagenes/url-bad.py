import pandas as pd
import requests

# Función para verificar si una URL está activa
def verificar_url(url):
    if not url:
        return False 
    try:
        response = requests.head(url)
        return response.ok
    except requests.ConnectionError:
        return False

# Cargar el archivo Excel
archivo_excel = "C:/Users/geffe/Desktop/codigo/PRODUCT-SCRAPING/primera-carga-vultec.xlsx"  # Cambia por el nombre de tu archivo Excel
df = pd.read_excel(archivo_excel)

# Lista para almacenar las URL que no funcionan
urls_no_funcionan = []

# Iterar sobre las filas del DataFrame
for index, fila in df.iterrows():
    # Reemplazar las comas por tuberías "|" y el código de escape "%7C" por "|"
    fila["url"] = fila["url"].replace(",", "|").replace("%7C", "|")
    
    # Dividir los enlaces por los separadores "|"
    urls = fila["url"].split("|")
    sku = fila["SKU"]
    for url in urls:
        if not verificar_url(url.strip()):
            urls_no_funcionan.append({"SKU": sku, "URL": url.strip()})
            print(url)

# Crear un DataFrame con las URL que no funcionan
df_urls_no_funcionan = pd.DataFrame(urls_no_funcionan)

# Guardar los datos en un archivo Excel
archivo_resultado = "urls_no_funcionan.xlsx"
df_urls_no_funcionan.to_excel(archivo_resultado, index=False)

print(f"Se han guardado las URL que no funcionan en '{archivo_resultado}'.")


