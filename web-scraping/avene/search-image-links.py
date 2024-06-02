import requests
from bs4 import BeautifulSoup
import pandas as pd
# Lee el archivo Excel
df = pd.read_excel("C:/Users/geffe/Documents/SILABUZ/nataly/avene/links.xlsx")

# Extrae la columna nombre como una lista de cadenas
urls_list = df["url"].tolist()
SKUs_list = df["SKU"].tolist()
web_name_list = df["web_name"].tolist()
img_ulr_list = []

for url in urls_list:
    # Hacer una solicitud a la página web
    response = requests.get(url)
    product_img_ulr_list = []
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Crear un objeto BeautifulSoup con el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')
    
        # Encontrar todos los divs con la clase específica
        imagen_divs = soup.find_all('div', class_='t4s_ratio t4s-product__media is-pswp-disable')
    
        # Iterar sobre cada div y encontrar los elementos <img>
        for div in imagen_divs:
            img_tags = div.find_all('img')
            
            for img in img_tags:
            # Verificar si los atributos width y height son iguales a 1000
                if img.get('width') == '1000' and img.get('height') == '1000':
                    url_img = "https:" + img["data-src"] + "000"
                    product_img_ulr_list.append(url_img)
        excel_url="|".join(product_img_ulr_list)
        img_ulr_list.append(excel_url)

    # Manejar la respuesta en caso de error
    else:
        print(f"Error en {url} la solicitud devolvió el código de estado {response.status_code}")

df = pd.DataFrame({'name': web_name_list, 'SKU': SKUs_list, 'url': img_ulr_list})

# Guardar el DataFrame en un archivo Excel
df.to_excel('C:/Users/geffe/Documents/SILABUZ/nataly/avene/links-img.xlsx', index=False)