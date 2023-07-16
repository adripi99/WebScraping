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
        """
    Extrae los atributos de un elemento dado.

    Args:
        elemento (WebElement): Elemento del producto.
        atributosP (bool): Indica si se deben extraer atributos en profundidad.

    Returns:
        dict: Diccionario con los atributos extraídos del producto.
        """
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
            try:
                url_elemento = elemento.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
                url = url_elemento.get_attribute('href')
                self.driver.get(url)
            except Exception as e:
                print("No se pudo entrar en profundidad")
            sleep(2)#esperamos a que cargue la página
            try:
                atributos_extraidos["Review"] = self.driver.find_element(by=By.XPATH, value='.//span[@id="acrCustomerReviewText"]').text
            except Exception as e:
                atributos_extraidos["Review"] = "No encontrado"

            try:
                atributos_extraidos["Vendedor"] = self.driver.find_element(By.XPATH, '//div[@tabular-attribute-name="Vendido por" and contains(@class, "tabular-buybox-text")]').text
            except Exception as e:
                atributos_extraidos["Vendedor"] = "No encontrado"

            try:
                atributos_extraidos["Estrellas"] = self.driver.find_element(By.XPATH, '//a[@role="button" and contains(@class, "a-popover-trigger")]/span[@class="a-size-base a-color-base"]').text
            except Exception as e:
                atributos_extraidos["Estrellas"] = "No encontrado"

            
    
            try:
                self.driver.back()
            except Exception as e:
                print("No se pudo volver para atrás")

        return atributos_extraidos

        
    
    def buscar_productos(self, categoria, num_productos,atributos_en_profundidad,atributos_a_extraer, log_callback=None):
        """
        Realiza la búsqueda de productos en la página de Amazon.

        Args:
            categoria (str): Categoría de productos a buscar.
            num_productos (int): Número de productos a buscar.
            atributos_en_profundidad (bool): Indica si se deben extraer atributos en profundidad.
            atributos_a_extraer (list): Lista de atributos a extraer de los productos.
            log_callback (func): Función de devolución de llamada para el registro de eventos.

        Returns:
            ColeccionProductos: Colección de productos encontrados.
        """
        try:
            self.configurar_navegador()
        except Exception as e:
            print("Fallo al configurar el navegador")
        try:
            url = self.obtener_url_amazon(categoria)
            self.driver.get(url)
        except Exception as e:
            print("Fallo al obtener la url")
        productos = ColeccionProductos(atributos_a_extraer)
        Numero_Productos = 0
        # Aceptar las cookies
        sleep(2)
        try:
            accept_button = self.driver.find_element(By.ID, 'sp-cc-accept')
            accept_button.click()
        except Exception as e:
                print("No se encontró el botón de aceptar")
        while Numero_Productos != num_productos:
            try:
                wait = WebDriverWait(self.driver, 10)
                elementosList = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
            except Exception as e:
                print("Fallo al obtener los elementos")
                self.cerrar_navegador()
                return productos
            for i in range(len(elementosList)):
                try:
                    elemento=self.driver.find_elements(By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')[i]
                    atributos_extraidos = self.extraer_atributos_producto(elemento,atributos_en_profundidad)
                    producto = AmazonProducto(**atributos_extraidos)
                    productos.agregar_producto(producto)
                    Numero_Productos += 1
                except Exception as e:
                    print("Fallo al obtener el elemento")
                if log_callback is not None:
                    try:
                        sleep(1)
                        log_callback(f"Producto Numero: {Numero_Productos}")
                        sleep(1)
                        log_callback(f"Producto agregado: {producto.Titulo} - {producto.Precio} - {producto.Asin}")
                        sleep(1)
                        log_callback(f"Restantes: {num_productos-Numero_Productos}")
                    except Exception as e:
                        print("Error al agregar el mensaje al registro:", str(e))
                
                if Numero_Productos == num_productos:
                    self.cerrar_navegador()
                    return productos

            try:
                if log_callback is not None:
                    try:
                        sleep(1)
                        log_callback(f"---Pasando de página---")
                    except Exception as e:
                        print("Error al agregar el mensaje al registro:", str(e))
                sleep(2) # Espaciamos las peticiones
                siguiente_pagina_url = self.driver.find_element(By.XPATH,'//a[contains(text(),"Siguiente")]').get_attribute('href')
                self.driver.get(siguiente_pagina_url)
            except:
                if log_callback is not None:
                    try:
                        sleep(1)
                        log_callback(f"Fin, no hay mas productos a extraer")
                        sleep(1)
                        log_callback(f"Producto totales agregados: {Numero_Productos}")
                    except Exception as e:
                        print("Error al agregar el mensaje al registro:", str(e))
                return productos

        return productos

    

    def obtener_url_amazon(self, categoria):
        """
        Obtiene la URL correspondiente a una categoría de productos en Amazon.

        Args:
            categoria (str): Categoría de productos.

        Returns:
            str: URL de la categoría en Amazon.
        """
        # Mapea cada categoría a una URL de Amazon
        categorias_urls = {
            "electrónica": "https://www.amazon.es/s?i=electronics&page=2",
            "moda": "https://www.amazon.es/s?i=fashion&page=2",
            "cocina": "https://www.amazon.es/s?i=kitchen&page=2",
            "ordenadores" :"https://www.amazon.es/s?i=computers&page=2"
            # -----------------Agrega más categorías Aquí-------------------------
        }
        return categorias_urls.get(categoria.lower())
