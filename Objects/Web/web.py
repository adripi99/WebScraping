from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
class Web:
    """
    Clase Web que representa una configuración de navegación web con Selenium.

    """
    def __init__(self,show_browser):
        """
        Inicializa una instancia de la clase Web.

        """
        self.driver_path = "Objects\Web\chromedriver.exe"
        self.show_browser=show_browser
    def configurar_navegador(self):
        """
        Configura el navegador web con las opciones especificadas.

        Args:
            show_browser (bool): Indica si se debe mostrar el navegador o ejecutar en modo headless.

        """
        service = Service(executable_path=self.driver_path)
        self.chrome_options = Options()
        if not self.show_browser:
            self.chrome_options.add_argument('--headless=new')  # Ocultar el navegador
        self.chrome_options.add_argument('--log-level=3')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        
    def cerrar_navegador(self):
        """
        Cierra el navegador web.

        """
        self.driver.close()
        self.driver.quit()

    def obtener_url(self, categoria):
        """
        Obtiene la URL específica de la web para la categoría especificada.

        Args:
            categoria (str): Categoría para la cual se desea obtener la URL.

        Returns:
            str: URL específica de la web para la categoría especificada.

        """
        raise NotImplementedError("El método 'obtener_url()' debe ser implementado por cada clase hija.")

    def extraer_atributos_producto(self, elemento, atributosP):
        """
        Extrae los atributos específicos del producto en la web correspondiente.

        Args:
            elemento: Elemento HTML del producto.
            atributosP (bool): Indica si se deben extraer atributos en profundidad.

        Returns:
            dict: Diccionario de atributos extraídos del producto.

        """
        raise NotImplementedError("El método 'extraer_atributos_producto()' debe ser implementado por cada clase hija.")

    def buscar_productos(self, categoria, num_productos, atributos_en_profundidad, atributos_a_extraer, log_callback=None):
        """
        Realiza la búsqueda y extracción de productos en la web correspondiente.

        Args:
            categoria (str): Categoría de productos a buscar.
            num_productos (int): Número de productos a extraer.
            atributos_en_profundidad (bool): Indica si se deben extraer atributos en profundidad.
            atributos_a_extraer (list): Lista de atributos a extraer de los productos.
            log_callback (func): Función de devolución de llamada para registrar mensajes de progreso (opcional).

        Returns:
            ColeccionProductos: Colección de productos extraídos.

        """
        raise NotImplementedError("El método 'buscar_productos()' debe ser implementado por cada clase hija.")
