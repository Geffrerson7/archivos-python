import requests
from bs4 import BeautifulSoup
import pandas as pd

# Crear listas para almacenar los SKU y las URL de las imágenes
sku_list = []
lista_url_img = []

# Iterar sobre las páginas de la URL
for i in range(1, 5):
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

                # Encontrar las imágenes y los SKU del producto
                images = product_soup.find_all('div', class_='v4kqzh media-wrapper-hook uok6tq')
                skus = product_soup.find_all('div', class_='SDLrh4')

                # Manejar las imágenes del producto
                if len(images) == 1:
                    lista_url_img.append(images[0]['href'])
                else:
                    # Unir todas las URL de imágenes con '|'
                    img_urls = "|".join(image['href'] for image in images)
                    lista_url_img.append(img_urls)

                # Manejar los SKU del producto
                for sku in skus:
                    sku_list.append(sku.text.replace("SKU: ", ""))

# Crear un DataFrame con las listas de SKU y URL de imágenes
df = pd.DataFrame({'SKU': sku_list, 'IMAGEN': lista_url_img})

# Guardar el DataFrame en un archivo Excel
excel_output = "C:/Users/geffe/Documents/SILABUZ/nataly/SCRAPING/datos_SARAID.xlsx"
df.to_excel(excel_output, index=False)
