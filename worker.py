from PyQt6.QtCore import QThread,pyqtSignal
from Objects.Web.aliexpress_web import AliexpressWeb
from Objects.Web.amazon_web import AmazonWeb
import os
from datetime import datetime
class Worker(QThread):
    """
    Clase Worker que realiza el trabajo de web scraping en un hilo aparte.

    Args:
        web (str): Nombre de la página web a escrapear.
        categoria (str): Categoría de productos a buscar.
        num_productos (int): Número de productos a buscar.
        atributos_a_extraer (list): Lista de atributos a extraer de los productos.
        atributos_en_profundidad (bool): Indica si se deben extraer atributos en profundidad.
        show_browser (bool): Indica si se debe mostrar el navegador durante el scraping.
        export_format (str): Formato de exportación de los resultados.
        log_callback (func): Función de devolución de llamada para el registro de eventos.
    """
    finished = pyqtSignal()
    def __init__(self, web, categoria, num_productos, atributos_a_extraer, atributos_en_profundidad, show_browser,export_format, log_callback):
        super().__init__()
        self.web=web
        self.categoria = categoria
        self.num_productos = num_productos
        self.atributos_en_profundidad = atributos_en_profundidad
        self.show_browser = show_browser
        self.running = True
        self.log_callback = log_callback
        self.export_format=export_format
        self.atributos_a_extraer=atributos_a_extraer
    def run(self):
        """
        Método que ejecuta el trabajo de web scraping.

        """
        web = None

        if self.web == "Amazon":
            web = AmazonWeb(self.show_browser)
        elif self.web == "Aliexpress":
            web = AliexpressWeb(self.show_browser)
        else:
            self.log_callback("Web no reconocida.")
            self.finished.emit()
            return
        productos = web.buscar_productos(self.categoria, self.num_productos,self.atributos_en_profundidad,self.atributos_a_extraer, self.log_callback)
        # exportar los Objects\Export
        directorio="Objects/Export/"+self.web+"/"+self.categoria+"/"
        os.makedirs(directorio, exist_ok=True)
        productos.exportar(self.export_format,directorio+str(datetime.now().timestamp())+"."+self.export_format)
        self.finished.emit()

    def stop(self):
        """
        Método que detiene la ejecución del trabajo.

        """
        self.running = False