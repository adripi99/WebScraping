import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel,QGridLayout, QVBoxLayout,QHBoxLayout, QWidget, QLineEdit, QPushButton, QComboBox, QTextEdit, QCheckBox, QListWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal,QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from Objects.Web.aliexpress_web import AliexpressWeb
from Objects.Web.amazon_web import AmazonWeb
from Objects.Productos.coleccion_productos import ColeccionProductos
import debugpy
from datetime import datetime
# Variables globales
#NOTA: DEF funciones codigo. triplecomillas descripcion y argumentos.extension vsc
jsondata={}
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
        productos.exportar(self.export_format,"Objects/Export/"+self.web+"/"+self.categoria+"/"+str(datetime.now().timestamp())+"."+self.export_format)
        self.finished.emit()
        self.stop

    def stop(self):
        """
        Método que detiene la ejecución del trabajo.

        """
        self.running = False

class MainWindow(QMainWindow):
    """
    Clase MainWindow que representa la interfaz de usuario principal.

    """
    def __init__(self):
        super().__init__()

        self.worker = None

        self.setWindowTitle("Web Scraper")
        self.setGeometry(100, 100, 400, 300)

        self.web_label = QLabel("Pagina Web:")
        self.web_combo = QComboBox()
       

        self.categoria_label = QLabel("Categoría:")
        self.categoria_combo = QComboBox()
       
    

        self.num_productos_label = QLabel("Número de productos:")
        self.num_productos_edit = QLineEdit()
        # validar para aceptar solo números enteros
        validator = QRegularExpressionValidator(QRegularExpression("[0-9]+"))
        self.num_productos_edit.setValidator(validator)


        self.available_products_list = QListWidget()  # Lista de atributos disponibles
        self.selected_products_list = QListWidget()  # Lista de atributos seleccionados

        self.move_to_selected_button = QPushButton(">")
        self.move_to_available_button = QPushButton("<")

       
        self.export_label = QLabel("Formato de exportación:")
        self.export_combo = QComboBox()
        formats = ["csv", "html", "feather", "parquet", "pickle"]
        for format in formats:
            self.export_combo.addItem(format)

        self.show_browser_checkbox = QCheckBox("Mostrar Navegador")

        self.start_button = QPushButton("Iniciar")

        self.log_text = QTextEdit()
        left_layout = QVBoxLayout()  # Layout para la columna izquierda
        right_layout = QHBoxLayout()  # Layout para la columna derecha

        left_layout.addWidget(self.web_label)
        left_layout.addWidget(self.web_combo)
        left_layout.addWidget(self.categoria_label)
        left_layout.addWidget(self.categoria_combo)
        left_layout.addWidget(self.num_productos_label)
        left_layout.addWidget(self.num_productos_edit)

        attribute_layout = QGridLayout()  # Layout en cuadrícula para la sección de atributos
        attribute_layout.addWidget(QLabel("Atributos Disponibles a extraer:"), 0, 0)  # Encima de la lista de atributos disponibles
        attribute_layout.addWidget(QLabel("Atributos Seleccionados:"), 0, 1)  # Encima de la lista de atributos seleccionados
        attribute_layout.addWidget(self.available_products_list, 1, 0)  # Lista de atributos disponibles
        attribute_layout.addWidget(self.selected_products_list, 1, 1)  # Lista de atributos seleccionados
        attribute_layout.addWidget(self.move_to_selected_button, 2, 0)  # Botón ">"
        attribute_layout.addWidget(self.move_to_available_button, 2, 1)  # Botón "<"
        left_layout.addLayout(attribute_layout)


        left_layout.addWidget(self.export_label)
        left_layout.addWidget(self.export_combo)
        left_layout.addWidget(self.show_browser_checkbox)
        left_layout.addWidget(self.start_button)
        left_layout.addWidget(self.log_text)

        main_layout = QVBoxLayout()  # Layout principal
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        #Eventos
    
        self.web_combo.currentTextChanged.connect(self.cambia_categoria)
        self.start_button.clicked.connect(self.start_scraping)
        self.move_to_selected_button.clicked.connect(self.move_to_selected)
        self.move_to_available_button.clicked.connect(self.move_to_available)

    def move_to_selected(self):
        """
        Mueve un atributo seleccionado de la lista de atributos disponibles a la lista de atributos seleccionados.

        """
        selected_item = self.available_products_list.currentItem()
        if selected_item is not None:
            self.available_products_list.takeItem(self.available_products_list.row(selected_item))
            self.selected_products_list.addItem(selected_item.text())

    def move_to_available(self):
        """
        Mueve un atributo seleccionado de la lista de atributos seleccionados a la lista de atributos disponibles.

        """
        selected_item = self.selected_products_list.currentItem()
        if selected_item is not None:
            self.selected_products_list.takeItem(self.selected_products_list.row(selected_item))
            self.available_products_list.addItem(selected_item.text())
    
    def start_scraping(self):
        """
        Inicia el proceso de web scraping con los parámetros especificados.

        """
        if self.worker is not None and self.worker.isRunning():
            self.worker.stop()
        web = self.web_combo.currentText()
        categoria = self.categoria_combo.currentText()
        num_productos_text = self.num_productos_edit.text()
        export_format = self.export_combo.currentText().lower()
        show_browser = self.show_browser_checkbox.isChecked()
        atributos_a_extraer = [self.selected_products_list.item(i).text() for i in range(self.selected_products_list.count())]
        atributos_en_profundidad= False
        if any(atributo in atributos_a_extraer for atributo, valor in jsondata[web].get("atributos", {}).items() if valor == 1):
            atributos_en_profundidad = True
        if not atributos_a_extraer:
            self.log_callback("Debe seleccionar al menos un atributo para extraer.")
            return
        try:
            num_productos = int(num_productos_text)
            if num_productos <= 0:
                self.log_callback("El número de productos debe ser mayor a cero.")
                return
        except ValueError:
            self.log_callback("Ingrese un número válido para el número de productos.")
            return
        self.start_button.setEnabled(False)  # Deshabilitar el botón de inicio
        self.worker = Worker(web, categoria, num_productos, atributos_a_extraer, atributos_en_profundidad, show_browser,export_format, self.log_callback)
        self.worker.finished.connect(self.scraping_finished)
        self.worker.start()
       
    def cambia_categoria(self):
        """
        Actualiza la lista de categorías disponibles según la página web seleccionada.

        """
        config = jsondata
        if self.web_combo.currentText() == '':
            webs = list(config.keys())
            for webi in webs:
                self.web_combo.addItem(webi.capitalize())
        web = self.web_combo.currentText()

        self.categoria_combo.clear()  # Vaciar el contenido de categoria_combo\
        self.available_products_list.clear()
        self.selected_products_list.clear()
        categoria_config = config[web].get("categorias", {})
        for categoria in categoria_config:
            self.categoria_combo.addItem(categoria.capitalize())
        
        Atributos=config[web].get("atributos", {})
        for atributo in Atributos:
            self.available_products_list.addItem(atributo.capitalize())
    def scraping_finished(self):
        """
        Se ejecuta cuando el proceso de web scraping ha finalizado.

        """
        self.log_callback("Búsqueda de productos finalizada.")
        self.start_button.setEnabled(True)  # Habilitar el botón de inicio
        #self.worker = None

    def log_callback(self, message):
        """
        Agrega un mensaje al registro de eventos en la interfaz de usuario.

        Args:
            message (str): Mensaje a agregar al registro.

        """
        self.log_text.append(message)
        
def load_config(file_path):
    """
    Lee la configuracion desde un .json

    Args:
         file_path (str): Ruta del fichero de configuracion.

        """
    with open(file_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    jsondata= load_config("Vista_config.json") #encoding utf
    window.cambia_categoria()
    window.show()
    sys.exit(app.exec())
