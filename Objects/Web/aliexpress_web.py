from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from Objects.Productos.coleccion_productos import ColeccionProductos
from Objects.Web.web import Web
from Objects.Productos.aliexpress_producto import AliexpressProducto
class AliexpressWeb(Web):
    def __init__(self, show_browser):
        super().__init__()

    def configurar_navegador(self):
        super().configurar_navegador()
    
    def extraer_atributos_producto(self, elemento, atributos, atributosP):
        atributos_extraidos = {}
        for atributo in atributos:
            try:
                if atributo == "titulo":
                    titulo = elemento.find_element(By.XPATH, './/a[@class="manhattan--titleText--WccSjUS"]').text
                    atributos_extraidos["titulo"] = titulo
                elif atributo == "precio":
                    precio = elemento.find_element(By.XPATH, './/a[@class="manhattan--price-sale--1CCSZfK""]').text
                    atributos_extraidos["precio"] = precio
            except Exception as e:
                atributos_extraidos[atributo] = "Error: " + str(e)
        
        for atributoP in atributosP:
            url = elemento.find_element(By.XPATH, './/a[@class="item-title"]').get_attribute('href')
            self.driver.get(url)
            try:
                if atributoP == "descripcion":
                    descripcion = self.driver.find_element(By.CSS_SELECTOR, 'div.product-description-container').text
                    atributos_extraidos["descripcion"] = descripcion
                elif atributoP == "vendedor":
                    vendedor = self.driver.find_element(By.CSS_SELECTOR, 'span.shop-name').text
                    atributos_extraidos["vendedor"] = vendedor
            except Exception as e:
                atributos_extraidos[atributoP] = "Error: " + str(e)
        
        return atributos_extraidos
    
    def buscar_productos(self, categoria, num_productos, atributos_a_extraer, atributos_en_profundidad, log_callback=None):
        self.configurar_navegador()
        url = self.obtener_url_aliexpress(categoria)
        self.driver.get(url)
        productos = ColeccionProductos()
        Numero_Productos = 0

        while Numero_Productos != num_productos:
            wait = WebDriverWait(self.driver, 10)
            elementos = wait.until(EC.presence_of_all_elements_located((By.XPATH, './/a[@class="item-title"]')))

            for elemento in elementos:
                atributos_extraidos = self.extraer_atributos_producto(elemento, atributos_a_extraer, atributos_en_profundidad)
                producto = AliexpressProducto(**atributos_extraidos)
                productos.agregar_producto(producto)
                if log_callback is not None:
                    log_callback(f"Producto Numero: {Numero_Productos}")
                    log_callback(f"Producto agregado: {producto.titulo} - {producto.precio} - {producto.asin}")
                    log_callback(f"Restantes: {num_productos-Numero_Productos}")
                Numero_Productos += 1
                if Numero_Productos == num_productos:
                    return productos

            try:
                sleep(3)  # Espaciamos las peticiones
                siguiente_pagina_url = self.driver.find_element(By.XPATH, '//a[contains(text(),"Siguiente")]').get_attribute('href')
                self.driver.get(siguiente_pagina_url)
            except:
                break

        return productos

    def obtener_url_aliexpress(self, categoria):
        categorias_urls = {
            "cocina": "https://es.aliexpress.com/category/204003396/kitchen-dining-bar.html?category_redirect=1",
            "ordenadores": "https://es.aliexpress.com/category/204000007/computer-office.html?category_redirect=1"
            # Agrega más categorías y sus respectivas URL
        }
        return categorias_urls.get(categoria.lower())
