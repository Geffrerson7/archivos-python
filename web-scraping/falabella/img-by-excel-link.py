"""Generar excel de URLs de imágenes de Falabella buscando por link"""
# Librerías
import time                                             # Para control de pausas                       # Para hermosear HTMLs
from selenium import webdriver                          # Para realizar web scraping
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys                                      # Para capturar información del error
import pandas as pd

# Lee el archivo Excel
df = pd.read_excel("C:/Users/geffe/Documents/SILABUZ/SCRAPING/links.xlsx")

# Extrae la columna SKU como una lista de cadenas
excel_skus_list = df["SKU"].astype(str).tolist()
excel_links_list = df["Link"].astype(str).tolist()
          
# Hacer una pausa en segundos para saltarse sleep de Python (le causa problemas al web driver)
def mySleep(nTimeOut):
    nTimeInit = time.time()
    nTimeDifference = time.time() - nTimeInit 
    while (nTimeDifference < nTimeOut):
        nTimeDifference = time.time() - nTimeInit

#
# MAIN
#
if (__name__ == '__main__'):
    # Lista de urls por SKU
    list_URLs_by_sku = []
    excel_img_url_list = []
    span_texts_by_sku = []
    # Configuración del Driver Selenium para Chrome 
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    for LINK in excel_links_list:
        # Ingresamos el SKU en el buscador de la página de Falabella
        driver.get(LINK)
        mySleep(2)
        
        # Buscar div donde está el span con la descripción del producto
        span_element = driver.find_element(By.XPATH, '//div[@class="fb-product-information-tab__copy"]')
        # Obtener el texto del span
        span_text = span_element.text
        span_texts_by_sku.append(span_text)

        # Buscar el div con clase "jsx-3040205320 hidden"
        div_elements = driver.find_elements(By.XPATH, '//div[@class="jsx-3040205320 hidden"]')
        # Buscar los elementos img dentro del div encontrado
        for div_element in div_elements:
            elements = div_element.find_elements(By.XPATH, './/img[@class="jsx-2487856160"]')

            for element in elements:
                list_URLs_by_sku.append(element.get_attribute("src"))
        URLS="|".join(list_URLs_by_sku)
        excel_img_url_list.append(URLS)
        # Crear un DataFrame con los SKU y las URLs
    df = pd.DataFrame({'SKU': excel_skus_list, 'url': excel_img_url_list, 'descripciones': span_texts_by_sku})

        # Guardar el DataFrame en un archivo Excel
    df.to_excel('C:/Users/geffe/Documents/SILABUZ/SCRAPING/lista_urls_img.xlsx', index=False)
