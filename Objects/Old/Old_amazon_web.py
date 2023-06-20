from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from Productos.amazon_producto import AmazonProducto
from Productos.coleccion_productos import ColeccionProductos

class AmazonWeb:
    def __init__(self, driver_path):
        chrome_options = Options()
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(driver_path, options=chrome_options)

    def buscar_productos(self, url, num_paginas):
        self.driver.get(url)
        productos = ColeccionProductos()
        for i in range(num_paginas):
            wait = WebDriverWait(self.driver, 10)
            #elementos = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".a-size-base-plus a-color-base a-text-normal")))
            sleep(6) # Esperamos a que cargue la página
            elementos= wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
            #elementos = self.driver.find_elements_by_css_selector(".s-card-container s-overflow-hidden aok-relative puis-wide-grid-style puis-wide-grid-style-t2 puis-expand-height puis-include-content-margin puis s-latency-cf-section s-card-border")
            for elemento in elementos:
             
                #titulo = elemento.find_element_by_xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]').text
                titulo = elemento.find_element(by=By.XPATH, value='.//span[@class="a-size-base-plus a-color-base a-text-normal"]').text
                #precio_str = elemento.find_element_by_xpath('.//span[@class="a-price-whole"]').text
                #precio= float(precio_str.replace(',', '.')) find_element(by=By.XPATH, value=xpath)
                #precio = (elemento.find_element(by=By.XPATH, value='//span[@class="a-price-whole"]')).text
                try:
                    precio= elemento.find_element_by_css_selector('span.a-price-whole').text
                except:
                    precio= "0,0"
                asin = elemento.get_attribute("data-asin")
                producto = AmazonProducto(titulo, precio, asin)
                productos.agregar_producto(producto)
            try:
                siguiente_pagina_url = self.driver.find_element_by_xpath('//a[contains(text(),"Siguiente")]').get_attribute('href')
                self.driver.get(siguiente_pagina_url)
            except:
                break
        return productos

    def cerrar_navegador(self):
        self.driver.quit()
        self.driver.close()

