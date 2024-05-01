# Librerías
import time 
import traceback                                            # Para control de pausas
from bs4 import BeautifulSoup                           # Para hermosear HTMLs
from selenium import webdriver                          # Para realizar web scraping
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
                                        

# Patrones de búsqueda
L_FIND = ['isdin']  
          
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

    # Configuración del Driver Selenium para Chrome 
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    # Recorremos lista de patrones de búsqueda
    for S_FIND in L_FIND:
        
        print('=' * len('Patrón de búsqueda: {}'.format(S_FIND)))
        print('Patrón de búsqueda: {}'.format(S_FIND))
        print('=' * len('Patrón de búsqueda: {}'.format(S_FIND)))

        # Ingresamos patrón de búsqueda
        driver.get('https://www.falabella.com.pe/falabella-pe')
        mySleep(2)
        inputText = driver.find_element(By.XPATH, '//*[@id="testId-SearchBar-Input"]')
        inputText.send_keys(S_FIND)
        inputText.send_keys(Keys.ENTER)
        mySleep(1)

        try:

            sXpath = '//div[@class="jsx-2481219049 jsx-2056183481"]'
            contentData = driver.find_elements(By.XPATH, sXpath)
            
            # for name in contentData:
            #     print(name.text)
            for name_div in contentData:
                # Encontrar el elemento b dentro del div para obtener el nombre
                name_elements = name_div.find_elements(By.TAG_NAME, "b")
                
                print(name_elements[1].text)
        except:

            traceback.print_exc()
        
    driver.close()
    driver.quit()

    