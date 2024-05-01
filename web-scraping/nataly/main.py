import requests, re
from bs4 import BeautifulSoup
import pandas as pd

# Leer el archivo Excel con las URLs
excel_file = "C:/Users/geffe/Documents/SILABUZ/nataly/SCRAPING/URL.xlsx"
df = pd.read_excel(excel_file)

# Lista para almacenar las descripciones
skus_total = []
nombres_total = []
hrefs_total = []

dimension_pattern = re.compile(r'/w_\d+,\w+,\w+,\w+/')

for url in df['URL']:
    response = requests.get(url)
    if response.status_code == 200:
        # Parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        names = soup.find_all('h1', class_='OXQzmM')
        skus = soup.find_all('div', class_='SDLrh4')
        hrefs = soup.find_all('div', class_='v4kqzh media-wrapper-hook uok6tq')
        
        for sku in skus:
            skus_total.append(sku.text.replace("SKU: ","").replace(".","-"))
        for name in names:
            nombres_total.append(name.text)
    
            
        if len(hrefs) == 1:
            for href in hrefs:
                # Obtener el enlace
                href_link = href['href']
                # Reemplazar las dimensiones en el enlace utilizando expresiones regulares
                new_href_link_1 = dimension_pattern.sub('/w_1000,h_1000,al_c,q_85/', href_link)
                new_href_link_2 = dimension_pattern.sub('/w_1000,h_1000,al_c,lg_1,q_85/', href_link)
                if requests.get(new_href_link_1).status_code == 200:
                    hrefs_total.append(new_href_link_1)
                elif requests.get(new_href_link_2).status_code == 200:
                    hrefs_total.append(new_href_link_2)
        else:
            href_string = '|'.join(dimension_pattern.sub('/w_1000,h_1000,al_c,q_85/', href['href']) for href in hrefs)
            hrefs_total.append(href_string)

    elif response.status_code == 403:
        print(f"Error: Forbidden (403) al acceder a la URL: {url}")
    else:
        print(f"Error: {response.status_code} al acceder a la URL: {url}")

df['SKU'] = skus_total
df['Nombre'] = nombres_total
df['Href'] = hrefs_total

# Guardar solo las columnas 'Nombre', 'SKU' y 'Href' en un nuevo archivo Excel
excel_output = "C:/Users/geffe/Documents/SILABUZ/nataly/SCRAPING/datos.xlsx"
df[['Nombre', 'SKU', 'Href']].to_excel(excel_output, index=False)
