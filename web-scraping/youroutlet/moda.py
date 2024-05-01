import requests
import pandas as pd
from bs4 import BeautifulSoup
import shutil

# Leer los SKUs del archivo Excel específico
excel_sku = "C:/Users/geffe/Documents/SILABUZ/SARAID/LISTA-SKU.xlsx" # Cambia esto por la ruta de tu archivo Excel de SKUs
sku_df = pd.read_excel(excel_sku)
skus_a_buscar = sku_df['SKU'].tolist()

# Crear listas para almacenar los SKUs encontrados y las URL de las imágenes
skus_encontrados = []
url_imagenes = []

# Iterar sobre las páginas de la URL
for i in range(1, 82):
    url = f"https://www.youroutlet.pe/moda?page={i}"
    response = requests.get(url)

    if response.status_code == 200:
        # Parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todos los enlaces de los productos en la página
        links = soup.find_all('a', class_='AJctir bGFTjD')

        # Iterar sobre los enlaces de los productos
        for product_link in links:
            product_response = requests.get(product_link['href'])

            if product_response.status_code == 200:
                # Parsear el HTML de la página del producto
                product_soup = BeautifulSoup(product_response.text, 'html.parser')

                # Encontrar las imágenes y los SKUs del producto
                images = product_soup.find_all('div', class_='v4kqzh media-wrapper-hook uok6tq')
                skus = product_soup.find_all('div', class_='SDLrh4')

                # Manejar las imágenes y los SKUs del producto
                for sku, image in zip(skus, images):
                    sku_text = sku.text.replace("SKU: ", "")
                    if sku_text in skus_a_buscar:
                        skus_encontrados.append(sku_text)
                        urls_imagenes = '|'.join([img['href'] for img in images])
                        url_imagenes.append(urls_imagenes)

# Crear un DataFrame con los SKUs encontrados y las URL de las imágenes
df_resultado = pd.DataFrame({'SKU': skus_encontrados, 'url': url_imagenes})

# Guardar el DataFrame en un archivo Excel
excel_output = "C:/Users/geffe/Documents/SILABUZ/SARAID/lista-a-d.xlsx"  # Cambia esto por la ruta donde quieres guardar el resultado
df_resultado.to_excel(excel_output, index=False)
