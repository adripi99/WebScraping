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
        super().__init__()

    def configurar_navegador(self):
        super().configurar_navegador()
    def extraer_atributos_producto(self, elemento,atributosP):
        atributos_extraidos = {}
        try:
            titulo = elemento.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]').text
            atributos_extraidos["titulo"] = titulo

            precio = elemento.find_element_by_css_selector('span.a-price-whole').text
            atributos_extraidos["precio"] = precio

            asin = elemento.get_attribute("data-asin")
            atributos_extraidos["asin"] = asin
        except Exception as e:
            atributos_extraidos[e] = "Error: " + str(e)
        #NOTA: sacar todo lo posible , profundidad si o no (binario) seleccionar al extraer
        if(atributosP):
            url = elemento.find_element(By.XPATH, './/a').get_attribute('href')#Entramos en el producto
            self.driver.get(url)
            try:
                    titulo = elemento.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]').text
                    atributos_extraidos["titulo"] = titulo
                    #descripcion = 
                    atributos_extraidos["descripcion"] = descripcion
                    #vendedor = 
                    atributos_extraidos["vendedor"] = vendedor
            except Exception as e:
                atributos_extraidos[e] = "Error: " + str(e)  
        return atributos_extraidos
    
    def buscar_productos(self, categoria, num_productos,atributos_en_profundidad, log_callback=None):
        self.configurar_navegador()
        url = self.obtener_url_amazon(categoria)
        self.driver.get(url)
        productos = ColeccionProductos()
        Numero_Productos = 0
        # Aceptar las cookies
        accept_button = self.find_element(By.ID, 'sp-cc-accept')
        accept_button.click()
        while Numero_Productos != num_productos:
            wait = WebDriverWait(self.driver, 10)
            elementos = wait.until(EC.presence_of_all_elements_located((By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]')))

            for elemento in elementos:
                atributos_extraidos = self.extraer_atributos_producto(elemento,atributos_en_profundidad)
                producto = AmazonProducto(**atributos_extraidos)
                productos.agregar_producto(producto)
                if log_callback is not None:
                    log_callback(f"Producto Numero: {Numero_Productos}")
                    log_callback(f"Producto agregado: {producto.titulo} - {producto.precio} - {producto.asin}")
                    log_callback(f"Restantes: {num_productos-Numero_Productos}")
                Numero_Productos += 1
                if Numero_Productos == num_productos:
                    return productos

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
