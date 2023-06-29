from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Web:
    def __init__(self):
        self.driver_path = "Objects\Web\chromedriver.exe"
    def configurar_navegador(self,show_browser):
        self.chrome_options = Options()
        if not show_browser:
            self.chrome_options.add_argument('--headless=new')  # Ocultar el navegador
        self.chrome_options.add_argument('--log-level=3')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(self.driver_path, options=self.chrome_options)