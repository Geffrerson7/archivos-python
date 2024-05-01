"""Generar excel de URLs de imágenes de Falabella buscando por SKU"""
# Librerías
import time                                             # Para control de pausas
from bs4 import BeautifulSoup                           # Para hermosear HTMLs
from selenium import webdriver                          # Para realizar web scraping
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys                                          # Para capturar información del error
import pandas as pd

# Lee el archivo Excel
df = pd.read_excel("C:/Users/geffe/Documents/SILABUZ/SCRAPING/SKU.xlsx")

# Extrae la columna SKU como una lista de cadenas
sku_list = df["SKU"].astype(str).tolist()

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
    excel_url_list = []
    # Configuración del Driver Selenium para Chrome 
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    # Recorremos lista de SKUs
    for SKU in sku_list:
        list_URLs = []
        # Ingresamos el SKU en el buscador de la página de Falabella
        driver.get('https://www.falabella.com.pe/falabella-pe')
        mySleep(2)
        inputText = driver.find_element(By.XPATH, '//*[@id="testId-SearchBar-Input"]')
        inputText.send_keys(SKU)
        inputText.send_keys(Keys.ENTER)
        mySleep(1)

        # Buscar el div con clase "jsx-3040205320 hidden"
        div_elements = driver.find_elements(By.XPATH, '//div[@class="jsx-3040205320 hidden"]')

        # Buscar los elementos img dentro del div encontrado
        for div_element in div_elements:
            elements = div_element.find_elements(By.XPATH, './/img[@class="jsx-2487856160"]')

            for element in elements:
            # Imprimir el src del elemento img
                list_URLs.append(element.get_attribute("src"))
        URLS="|".join(list_URLs)
        excel_url_list.append(URLS)
        # Crear un DataFrame con los SKU y las URLs
    df = pd.DataFrame({'SKU': sku_list, 'url': excel_url_list})

    # Guardar el DataFrame en un archivo Excel
    df.to_excel('C:/Users/geffe/Documents/SILABUZ/SCRAPING/SKU_URLs.xlsx', index=False)