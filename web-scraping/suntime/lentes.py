import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_excel("C:/Users/geffe/Desktop/lista-suntime.xlsx")

# Extrae la columna SKU como una lista de cadenas

excel_skus_list = df["SKU"].astype(str).tolist()
excel_links_list = df["Link"].astype(str).tolist()
excel_names_list = []
excel_colors_list = []
excel_web_sku_list = []
for link in excel_links_list:
    # Realizar una solicitud GET a la URL
    response = requests.get(link)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Crear el objeto BeautifulSoup con el contenido de la página y el parser html.parser
        soup = BeautifulSoup(response.content, 'html.parser')
        name_element = soup.find('h1', class_='text-2xl md:text-3xl md:leading-[42px] pr-2')
        excel_names_list.append(name_element.text)
        color_element = soup.find('span', class_='selected-value option-label')
        excel_colors_list.append(color_element.text.upper())
        web_sku_element = soup.find('div', class_ = "prod__additional_infos-value prod__sku")
        excel_web_sku_list.append(web_sku_element.text)


df = pd.DataFrame({'SKU': excel_skus_list, 'name': excel_names_list, 'color': excel_colors_list, 'web sku': excel_web_sku_list})

# Guardar el DataFrame en un archivo Excel
df.to_excel("C:/Users/geffe/Desktop/lista-especificaciones.xlsx", index=False)