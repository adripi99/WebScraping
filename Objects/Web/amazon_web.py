from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from Objects.Productos.amazon_producto import AmazonProducto
from Objects.Productos.coleccion_productos import ColeccionProductos
from Objects.Web.web import Web
from selenium.webdriver.chrome.options import Options

class AmazonWeb(Web):
    def __init__(self, show_browser):
        super().__init__(show_browser)

    def extraer_atributos_producto(self, elemento, atributosP):
        atributos_extraidos = {}
        try:
            titulo = elemento.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]').text
            atributos_extraidos["Titulo"] = titulo
        except Exception as e:
            atributos_extraidos["Titulo"] = "No encontrado"

        try:
            precio = elemento.find_element(By.CSS_SELECTOR,'span.a-price-whole').text
            atributos_extraidos["Precio"] = precio
        except Exception as e:
            atributos_extraidos["Precio"] = "No encontrado"

        try:
            asin = elemento.get_attribute("data-asin")
            atributos_extraidos["Asin"] = asin
        except Exception as e:
            atributos_extraidos["Asin"] = "No encontrado"

        if atributosP:
            url_elemento = elemento.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
            url = url_elemento.get_attribute('href')
            self.driver.get(url)
            try:
                atributos_extraidos["Review"] = self.driver.find_element(by=By.XPATH, value='.//span[@id="acrCustomerReviewText"]').text
            except Exception as e:
                atributos_extraidos["Review"] = "No encontrado"

            try:
                atributos_extraidos["Vendedor"] = self.driver.find_element(By.XPATH, './/span[@class="a-size-small tabular-buybox-text-message"]').text
            except Exception as e:
                atributos_extraidos["Vendedor"] = "No encontrado"

            try:
                atributos_extraidos["Estrellas"] = self.driver.find_element(By.XPATH, './/span[@class="a-size-base a-color-base"]').text
            except Exception as e:
                atributos_extraidos["Estrellas"] = "No encontrado"

            self.driver.back()
    
            accept_button = self.driver.find_element(By.ID, 'sp-cc-accept')
            accept_button.click()

        return atributos_extraidos

        
    
    def buscar_productos(self, categoria, num_productos,atributos_en_profundidad,atributos_a_extraer, log_callback=None):
        self.configurar_navegador()
        url = self.obtener_url_amazon(categoria)
        self.driver.get(url)
        productos = ColeccionProductos(atributos_a_extraer)
        Numero_Productos = 0
        # Aceptar las cookies
        sleep(3)
        accept_button = self.driver.find_element(By.ID, 'sp-cc-accept')
        accept_button.click()
        while Numero_Productos != num_productos:
            wait = WebDriverWait(self.driver, 10)
            elementosList = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
            for i in range(len(elementosList)):
                elemento=self.driver.find_elements(By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')[i]
                atributos_extraidos = self.extraer_atributos_producto(elemento,atributos_en_profundidad)
                #print(atributos_extraidos)
                producto = AmazonProducto(**atributos_extraidos)
                productos.agregar_producto(producto)
                Numero_Productos += 1
                if log_callback is not None:
                    log_callback(f"Producto Numero: {Numero_Productos}")
                    log_callback(f"Producto agregado: {producto.Titulo} - {producto.Precio} - {producto.Asin}")
                    log_callback(f"Restantes: {num_productos-Numero_Productos}")
                
                if Numero_Productos == num_productos:
                    self.driver.close()
                    return productos

            try:
                sleep(3) # Espaciamos las peticiones
                siguiente_pagina_url = self.driver.find_element_by_xpath('//a[contains(text(),"Siguiente")]').get_attribute('href')
                self.driver.get(siguiente_pagina_url)
            except:
                if log_callback is not None:
                    log_callback(f"Fin, no hay mas productos a extraer")
                    log_callback(f"Producto totales agregados: {Numero_Productos}")
                return productos

        return productos

    

    def obtener_url_amazon(self, categoria):
        # Mapea cada categoría a una URL de Amazon
        categorias_urls = {
            "electrónica": "https://www.amazon.es/s?i=electronics&page=2",
            "moda": "https://www.amazon.es/s?i=fashion&page=2",
            "cocina": "https://www.amazon.es/s?i=kitchen&page=2",
            "ordenadores" :"https://www.amazon.es/s?i=computers&page=2"
            # -----------------Agrega más categorías-------------------------
        }
        return categorias_urls.get(categoria.lower())
