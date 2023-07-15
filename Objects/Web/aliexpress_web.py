from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from Objects.Productos.coleccion_productos import ColeccionProductos
from Objects.Web.web import Web
from Objects.Productos.aliexpress_producto import AliexpressProducto
from selenium.webdriver.common.keys import Keys
class AliexpressWeb(Web):
    def __init__(self, show_browser):
        super().__init__(show_browser)
    
    def extraer_atributos_producto(self, elemento, atributosP,i):
        atributos_extraidos = {}
        try:
            titulo = elemento.find_element(By.XPATH, './/h1[@class="manhattan--titleText--WccSjUS"]').text
            atributos_extraidos["Titulo"] = titulo
        except Exception as e:
            atributos_extraidos["Titulo"] = "No encontrado"

        try:
            precio_elemento = self.driver.find_elements(By.CLASS_NAME,'manhattan--price-sale--1CCSZfK')[i]
            #precio_elemento = self.driver.find_element_by_class_name('manhattan--price-sale--1CCSZfK')
            precio = precio_elemento.text.replace(',', '.')
            atributos_extraidos["Precio"] = precio
        except Exception as e:
            atributos_extraidos["Precio"] = "No encontrado"

        if atributosP:
            url_elemento = self.driver.find_elements(By.XPATH, '//a[contains(@class,"earch-card-item")]')[i]
            url = url_elemento.get_attribute('href')
            self.driver.get(url)
            try:
                atributos_extraidos["Estrellas"] = self.driver.find_element(By.XPATH, './/div[@class="ae-header-content-num"]').text

            except Exception as e:
                atributos_extraidos["Estrellas"] = "No tiene estrellas"

            try:
                atributos_extraidos["Vendedor"] = self.driver.find_element(By.XPATH, './/a[@class="store-header--storeName--vINzvPw"]').text
            except Exception as e:
                atributos_extraidos["Vendedor"] = "No encontrado"

            self.driver.back()
        return atributos_extraidos
    
    def buscar_productos(self, categoria, num_productos,atributos_en_profundidad,atributos_a_extraer, log_callback=None):
        self.configurar_navegador()
        url = self.obtener_url_aliexpress(categoria)
        self.driver.get("https://es.aliexpress.com")
        sleep(1)
        accept_button = self.driver.find_element(By.XPATH, './/button[@class="btn-accept"]')
        accept_button.click()
        sleep(1)
        self.driver.get(url)
        self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
        self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
        productos = ColeccionProductos(atributos_a_extraer)
        Numero_Productos = 0

        while Numero_Productos != num_productos:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
            self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
            wait = WebDriverWait(self.driver, 20)
            elementosList = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[contains(@class,"earch-card-item")]')))

            for i in range(len(elementosList)):
                print(i)
                try:
                    elemento=self.driver.find_elements(By.XPATH, '//a[contains(@class,"earch-card-item")]')[i]
                except:
                    self.driver.refresh()
                    sleep(1)
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
                    sleep(1)
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
                    sleep(1)
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
                    sleep(1)
                    wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[contains(@class,"earch-card-item")]')))
                    try:
                     elemento=self.driver.find_elements(By.XPATH, '//a[contains(@class,"earch-card-item")]')[i]
                    except:
                        if log_callback is not None:
                            try:
                                sleep(1)
                                log_callback(f"Error, no se puede extraer mas productos")
                                sleep(1)
                                log_callback(f"Producto totales agregados: {Numero_Productos}")
                                sleep(2)
                                return productos
                            except Exception as e:
                                print("Error al agregar el mensaje al registro:", str(e))
                                return productos
                        print("Error al encontrar el elemento:"+str(i))
                        return productos
                atributos_extraidos = self.extraer_atributos_producto(elemento,atributos_en_profundidad,i)
                producto = AliexpressProducto(**atributos_extraidos)
                #print(atributos_extraidos)
                productos.agregar_producto(producto)
                Numero_Productos += 1
                if log_callback is not None:
                    try:
                        sleep(1)
                        log_callback(f"Producto Numero: {Numero_Productos}")
                        sleep(1)
                        log_callback(f"Producto agregado: {producto.Titulo} - {producto.Precio}")
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
                sleep(3)  # Espaciamos las peticiones
                Burl=self.driver.find_element(By.XPATH, '//li[contains(text(),"Siguiente")]')
                Burl.click()
                sleep(2)
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

    def obtener_url_aliexpress(self, categoria):
        categorias_urls = {
            "cocina": "https://es.aliexpress.com/category/204000021/consumer-electronics.html",
            "ordenadores": "https://es.aliexpress.com/category/204000007/computer-office.html?category_redirect=1"
            # Agrega más categorías y sus respectivas URL
        }
        return categorias_urls.get(categoria.lower())
