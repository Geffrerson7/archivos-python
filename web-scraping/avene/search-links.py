import time                        
from selenium import webdriver                          
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
# Lee el archivo Excel
df = pd.read_excel("C:/Users/geffe/Documents/SILABUZ/nataly/avene/nombres.xlsx")

# Extrae la columna nombre como una lista de cadenas
name_list = df["nombre"].tolist()
SKU_list = df["SKU"].tolist()
links_list = []
web_name_list = []

def mySleep(nTimeOut):
    nTimeInit = time.time()
    nTimeDifference = time.time() - nTimeInit 
    while (nTimeDifference < nTimeOut):
        nTimeDifference = time.time() - nTimeInit
        
if (__name__ == '__main__'):

    # Configuración del Driver Selenium para Chrome 
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    for name in name_list:
        driver.get('https://aveneperu.com/search')
        mySleep(2)
        inputText = driver.find_element(By.XPATH, '//input[@class="t4s-search-form__input js_iput_search col"]')
        inputText.send_keys(name)
        inputText.send_keys(Keys.ENTER)
        mySleep(2)
        products_list_div = driver.find_element(By.XPATH, '//div[@class="t4s_box_pr_grid t4s-products t4s-text-default t4s_rationt  t4s_position_8 t4s_cover t4s-row t4s-justify-content-center t4s-row-cols-lg-4 t4s-row-cols-md-2 t4s-row-cols-2 t4s-gx-md-30 t4s-gy-md-30 t4s-gx-10 t4s-gy-10"]')
        # Obtiene el primer div dentro de products_list_div
        first_product_div = products_list_div.find_element(By.XPATH, './/div[1]')
        a = first_product_div.find_element(By.XPATH, '//a[@class="t4s-full-width-link"]')
        web_name = first_product_div.find_element(By.XPATH, '//h3[@class="t4s-product-title"]')
        web_name_list.append(web_name.text)
        links_list.append(a.get_attribute("href"))
    driver.quit()

df = pd.DataFrame({'name': name_list, 'web_name': web_name_list, 'url': links_list,  'SKU': SKU_list})

# Guardar el DataFrame en un archivo Excel
df.to_excel('C:/Users/geffe/Documents/SILABUZ/nataly/avene/links.xlsx', index=False)