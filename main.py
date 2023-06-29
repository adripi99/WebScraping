import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QComboBox, QTextEdit, QCheckBox, QListWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from Objects.Web.aliexpress_web import AliexpressWeb
from Objects.Web.amazon_web import AmazonWeb
from Objects.Productos.coleccion_productos import ColeccionProductos
import debugpy
from datetime import datetime
# Variables globales
#NOTA: DEF funciones codigo. triplecomillas descripcion y argumentos.extension vsc
jsondata={}
class Worker(QThread):
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
        # exportar los 
        productos.exportar(self.export_format,"C:/Users/adrip/Desktop/VSC/Seleniumtfg2023/Objects/Export/"+datetime.now().strftime('%Y-%m-%d')+"."+self.export_format)

        self.log_callback("Búsqueda de productos finalizada.")

    def stop(self):
        self.running = False

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.worker = None

        self.setWindowTitle("Web Scraper")
        self.setGeometry(100, 100, 400, 300)

        self.web_label = QLabel("Pagina Web:")
        self.web_combo = QComboBox()
        self.web_combo.addItem("Amazon")
        self.web_combo.addItem("Aliexpress")

        self.categoria_label = QLabel("Categoría:")
        self.categoria_combo = QComboBox()
       
    

        self.num_productos_label = QLabel("Número de productos:")
        self.num_productos_edit = QLineEdit()
        #Directamete no permitir


        self.available_products_list = QListWidget()  # Lista de atributos disponibles
        self.selected_products_list = QListWidget()  # Lista de atributos seleccionados

        self.move_to_selected_button = QPushButton(">")
        self.move_to_available_button = QPushButton("<")

       
        self.export_label = QLabel("Formato de exportación:")
        self.export_combo = QComboBox()
        self.export_combo.addItem("csv")
        self.export_combo.addItem("excel")
        self.export_combo.addItem("html")
        self.export_combo.addItem("hdf")
        self.export_combo.addItem("feather")
        self.export_combo.addItem("parquet")
        self.export_combo.addItem("pickle")

        self.show_browser_checkbox = QCheckBox("Mostrar Navegador")

        self.start_button = QPushButton("Iniciar")

        self.log_text = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.web_label)
        layout.addWidget(self.web_combo)
        layout.addWidget(self.categoria_label)
        layout.addWidget(self.categoria_combo)
        layout.addWidget(self.num_productos_label)
        layout.addWidget(self.num_productos_edit)
        layout.addWidget(QLabel("Atributos Disponibles a extraer:")) # NOTA: Horizontal layout con adwidget con un sublayout 
        layout.addWidget(self.available_products_list)
        layout.addWidget(self.move_to_selected_button)
        layout.addWidget(self.move_to_available_button)
        layout.addWidget(QLabel("Atributos Seleccionados:"))
        layout.addWidget(self.selected_products_list)
        layout.addWidget(self.export_label)
        layout.addWidget(self.export_combo)
        layout.addWidget(self.show_browser_checkbox)
        layout.addWidget(self.start_button)
        layout.addWidget(self.log_text)
        


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        #Eventos
        self.web_combo.currentTextChanged.connect(self.cambia_categoria)
        self.start_button.clicked.connect(self.start_scraping)
        self.move_to_selected_button.clicked.connect(self.move_to_selected)
        self.move_to_available_button.clicked.connect(self.move_to_available)

    def move_to_selected(self):
        selected_item = self.available_products_list.currentItem()
        if selected_item is not None:
            self.available_products_list.takeItem(self.available_products_list.row(selected_item))
            self.selected_products_list.addItem(selected_item.text())

    def move_to_available(self):
        selected_item = self.selected_products_list.currentItem()
        if selected_item is not None:
            self.selected_products_list.takeItem(self.selected_products_list.row(selected_item))
            self.available_products_list.addItem(selected_item.text())
    
    def start_scraping(self):
        if self.worker is not None and self.worker.isRunning():
            self.worker.stop()

        web = self.web_combo.currentText()
        categoria = self.categoria_combo.currentText()
        num_productos = int(self.num_productos_edit.text())
        export_format = self.export_combo.currentText().lower()
        show_browser = self.show_browser_checkbox.isChecked()
        atributos_a_extraer = [self.selected_products_list.item(i).text() for i in range(self.selected_products_list.count())]
        atributos_en_profundidad= False
        if 1 in jsondata[web].get("atributos", {}).values():
            atributos_en_profundidad = True
            
        self.worker = Worker(web, categoria, num_productos, atributos_a_extraer, atributos_en_profundidad, show_browser,export_format, self.log_callback)
        self.worker.finished.connect(self.scraping_finished)
        self.worker.start()
    def cambia_categoria(self):
        web = self.web_combo.currentText()
        config = jsondata
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
        self.worker = None

    def log_callback(self, message):
        self.log_text.append(message)
        
def load_config(file_path):
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
