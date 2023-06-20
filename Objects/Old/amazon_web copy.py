from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from Productos.amazon_producto import AmazonProducto
from Productos.coleccion_productos import ColeccionProductos
from Web.web import Web
from selenium.webdriver.chrome.options import Options

class AmazonWeb(Web):
    def __init__(self, show_browser):
        super().__init__()

    def configurar_navegador(self):
        super().configurar_navegador()

    def buscar_productos(self, categoria, num_productos,log_callback=None):
        self.configurar_navegador()
        url = self.obtener_url_amazon(categoria)
        self.driver.get(url)
        productos = ColeccionProductos()
        Numero_Productos = 0
        while Numero_Productos != num_productos:
            wait = WebDriverWait(self.driver, 10)
            #sleep(6) # Esperamos a que cargue la página
            
            #elementos = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
            elementos = wait.until(EC.presence_of_all_elements_located((By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]')))
            #elementos = self.driver.find_elements(By.XPATH, './/div[contains("s-result-item s-asin")]')

            for elemento in elementos: 
                try:
                    titulo = elemento.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]').text
                except:
                    titulo = "NA"
                try:
                    precio = elemento.find_element_by_css_selector('span.a-price-whole').text
                except:
                    precio = "0,0"
                asin = elemento.get_attribute("data-asin")
                producto = AmazonProducto(titulo, precio, asin)
                productos.agregar_producto(producto)
                if log_callback is not None:
                    log_callback(f"Producto Numero: {Numero_Productos}")
                    log_callback(f"Producto agregado: {producto.titulo} - {producto.precio} - {producto.asin}")
                    log_callback(f"Restantes: {num_productos-Numero_Productos}")
                Numero_Productos += 1
                if Numero_Productos == num_productos:
                    break
            try:
                sleep(3) # Espaciamos las peticiones
                siguiente_pagina_url = self.driver.find_element_by_xpath('//a[contains(text(),"Siguiente")]').get_attribute('href')
                self.driver.get(siguiente_pagina_url)
            except:
                break
        return productos

    def obtener_url_amazon(self, categoria):
        # Mapea cada categoría a una URL de Amazon
        categorias_urls = {
            "electrónica": "https://www.amazon.es/s?i=electronics&page=2",
            "moda": "https://www.amazon.es/s?i=fashion&page=2",
            "Cocina": "https://www.amazon.es/s?i=kitchen&page=2",
            "Ordenadores" :"https://www.amazon.es/s?i=computers&page=2"
            # -----------------Agrega más categorías-------------------------
        }
        return categorias_urls.get(categoria.lower())
