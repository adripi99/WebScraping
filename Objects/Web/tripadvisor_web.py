from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from Objects.Productos.coleccion_productos import ColeccionProductos
from Objects.Productos.tripadvisor_productos import TripadvisorProducto
from Objects.Web.web import Web

class TripadvisorWeb(Web):
    """
    Clase que representa un web scraper para Tripadvisor.

    Args:
        show_browser (bool): Indica si se debe mostrar el navegador durante el scraping.

    Attributes:
        driver_path (str): Ruta del controlador del navegador.
        show_browser (bool): Indica si se debe mostrar el navegador durante el scraping.
        driver: Instancia del controlador del navegador.

    """

    def __init__(self, show_browser):
        super().__init__()
        self.show_browser = show_browser

    def configurar_navegador(self):
        """
        Configura el navegador web con las opciones especificadas.

        """
        super().configurar_navegador(self.show_browser)

    def extraer_atributos_hotel(self, elemento, atributosP):
        """
        Extrae los atributos de un hotel específico.

        Args:
            elemento: Elemento del DOM que representa un hotel en Tripadvisor.
            atributosP (bool): Indica si se deben extraer atributos en profundidad.

        Returns:
            dict: Diccionario con los atributos extraídos del hotel.

        """
        atributos_extraidos = {}

        try:
            nombre = elemento.find_element(By.XPATH, './/div[contains(@class, " Wd o W")]').text
            atributos_extraidos["Nombre"] = nombre
        except Exception as e:
            atributos_extraidos["Nombre"] = "No encontrado"

        try:
            direccion_elemento = elemento.find_element(By.XPATH, './/span[contains(@class, "addressText")]')
            direccion = direccion_elemento.text
            atributos_extraidos["Direccion"] = direccion
        except Exception as e:
            atributos_extraidos["Direccion"] = "No encontrada"

        if atributosP:
            try:
                telefono_elemento = elemento.find_element(By.XPATH, './/div[contains(@class, "phone")]//span')
                telefono = telefono_elemento.get_attribute("data-tel-number")
                atributos_extraidos["Telefono"] = telefono
            except Exception as e:
                atributos_extraidos["Telefono"] = "No encontrado"

            try:
                opiniones_elemento = elemento.find_element(By.XPATH, './/a[contains(@class, "review_count")]')
                opiniones = opiniones_elemento.text
                atributos_extraidos["Opiniones"] = opiniones
            except Exception as e:
                atributos_extraidos["Opiniones"] = "No encontradas"

            # Agregar más atributos en profundidad aquí

        return atributos_extraidos

    def buscar_productos(self, destino, num_hoteles, atributos_en_profundidad,atributos_a_extraer, log_callback=None):
        """
        Busca hoteles en Tripadvisor para un destino específico.

        Args:
            destino (str): Destino para buscar hoteles.
            num_hoteles (int): Número de hoteles a buscar.
            atributos_en_profundidad (bool): Indica si se deben extraer atributos en profundidad.
            log_callback (func): Función de devolución de llamada para el registro de eventos.

        Returns:
            ColeccionProductos: Colección de hoteles extraídos.

        """
        self.configurar_navegador()
        url = self.obtener_url_tripadvisor(destino)
        self.driver.get(url)
        hoteles = ColeccionProductos(atributos_a_extraer)
        numero_hoteles = 0

        while numero_hoteles < num_hoteles:
            wait = WebDriverWait(self.driver, 10)
            elementos_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@data-automation, "hotel-card-title")]')))

            for i in range(len(elementos_list)):
                elemento = self.driver.find_elements(By.XPATH, '//div[contains(@data-automation, "hotel-card-title")]')[i]
                atributos_extraidos = self.extraer_atributos_hotel(elemento, atributos_en_profundidad)
                hotel = TripadvisorProducto(**atributos_extraidos)
                hoteles.agregar_producto(hotel)
                numero_hoteles += 1
                if log_callback is not None:
                    log_callback(f"Hotel Número: {numero_hoteles}")
                    log_callback(f"Hotel Agregado: {hotel.Nombre} - {hotel.Direccion}")
                    log_callback(f"Restantes: {num_hoteles - numero_hoteles}")

                if numero_hoteles == num_hoteles:
                    self.driver.close()
                    return hoteles

            try:
                sleep(3)  # Espaciamos las peticiones
                siguiente_pagina_url = self.driver.find_element(By.XPATH, '//a[contains(@class, "next")]').get_attribute('href')
                self.driver.get(siguiente_pagina_url)
            except:
                if log_callback is not None:
                    log_callback("Fin, no hay más hoteles para extraer")
                    log_callback(f"Hoteles Totales Agregados: {numero_hoteles}")
                return hoteles

        return hoteles

    def obtener_url_tripadvisor(self, destino):
        """
        Obtiene la URL de búsqueda de hoteles en Tripadvisor para un destino específico.

        Args:
            destino (str): Destino para buscar hoteles.

        Returns:
            str: URL de búsqueda de hoteles en Tripadvisor.

        """
        url_base = "https://www.tripadvisor.com/"
        url_busqueda = f"{url_base}Hotels-g187451-Gijon_Asturias-Hotels.html"
        return url_busqueda

