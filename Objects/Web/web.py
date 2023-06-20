from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Web:
    def __init__(self,show_browser):
        self.driver_path = "C:/Users/adrip/Desktop/VSC/Seleniumtfg2023/Objects/chromedriver.exe"
        self.driver = None
        self.driver_options= None
        self.show_browser = show_browser
    def configurar_navegador(self):
        if self.show_browser:
            self.chrome_options.add_argument('--headless')  # Ocultar el navegador
        self.chrome_options = Options()
        self.chrome_options.add_argument('--log-level=3')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--ignore-ssl-errors')
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-popup-blocking")
        # chrome_options.add_argument("--disable-notifications")
        # chrome_options.add_argument("--disable-infobars")
        # chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--disable-web-security")

        # # Agregar encabezados personalizados
        #chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36")
        #chrome_options.add_argument("--accept-language=en-US,en;q=0.9")


        self.driver = webdriver.Chrome(self.driver_path, options=self.chrome_options)

    def cerrar_navegador(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None