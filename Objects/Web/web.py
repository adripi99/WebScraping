from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Web:
    """
    Clase Web que representa una configuración de navegación web con Selenium.

    """
    def __init__(self):
        """
        Inicializa una instancia de la clase Web.

        """
        self.driver_path = "Objects\Web\chromedriver.exe"
    def configurar_navegador(self,show_browser):
        """
        Configura el navegador web con las opciones especificadas.

        Args:
            show_browser (bool): Indica si se debe mostrar el navegador o ejecutar en modo headless.

        """
        self.chrome_options = Options()
        if not show_browser:
            self.chrome_options.add_argument('--headless=new')  # Ocultar el navegador
        self.chrome_options.add_argument('--log-level=3')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(self.driver_path, options=self.chrome_options)