import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QComboBox, QTextEdit, QCheckBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from Web.amazon_web import AmazonWeb
from Productos.coleccion_productos import ColeccionProductos

class Worker(QThread):
    finished = pyqtSignal()

    def __init__(self, categoria, num_productos, export_format, show_browser, log_callback):
        super().__init__()
        self.categoria = categoria
        self.num_productos = num_productos
        self.export_format = export_format
        self.show_browser = show_browser
        self.running = True
        self.log_callback = log_callback

    def run(self):
        # obtener los productos
        #print(self.show_browser)
        web=AmazonWeb(self.show_browser)
        productos = web.buscar_productos(self.categoria, self.num_productos, self.log_callback)

        # exportar los productos
        productos.exportar(self.export_format,ruta="./")
        

        self.log_callback("Búsqueda de productos finalizada.")

    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = None

        self.setWindowTitle("Amazon Web Scraper")
        self.setGeometry(100, 100, 400, 300)

        self.categoria_label = QLabel("Categoría:")
        self.categoria_combo = QComboBox()

        self.num_productos_label = QLabel("Número de productos:")
        self.num_productos_edit = QLineEdit()

        self.export_label = QLabel("Formato de exportación:")
        self.export_combo = QComboBox()

        self.show_browser_checkbox = QCheckBox("Mostrar Navegador")

        self.start_button = QPushButton("Iniciar")

        self.log_text = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.categoria_label)
        layout.addWidget(self.categoria_combo)
        layout.addWidget(self.num_productos_label)
        layout.addWidget(self.num_productos_edit)
        layout.addWidget(self.export_label)
        layout.addWidget(self.export_combo)
        layout.addWidget(self.show_browser_checkbox)
        layout.addWidget(self.start_button)
        layout.addWidget(self.log_text)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.start_button.clicked.connect(self.start_scraping)

    def start_scraping(self):
        if self.worker is not None and self.worker.isRunning():
            self.worker.stop()

        categoria = self.categoria_combo.currentText().lower()
        num_productos = int(self.num_productos_edit.text())
        export_format = self.export_combo.currentText().lower()
        show_browser = self.show_browser_checkbox.isChecked()

        config = load_config("config.json")
        export_formats_config = config.get("export_formats", {})
        categoria_config = config.get("categorias", {})
        ruta_config = config.get("ruta", "")

        if export_format in export_formats_config and export_formats_config[export_format] == 1:
            export_format_value = export_formats_config[export_format]
        else:
            export_format_value = 0

        if categoria in categoria_config and categoria_config[categoria] == 1:
            categoria_value = categoria_config[categoria]
        else:
            categoria_value = 0

        self.worker = Worker(categoria_value, num_productos, export_format_value, show_browser, ruta_config, self.log_callback)
        self.worker.finished.connect(self.scraping_finished)
        self.worker.start()

def log_callback(self, message):
    self.log_text.append(message)
def load_config(file_path):
    with open(file_path, "r") as f:
        config = json.load(f)
    return config
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    config = load_config("Vista_config.json") #encoding utf
    categoria_config = config.get("categorias", {})
    export_formats_config = config.get("export_formats", {})
    ruta_config = config.get("ruta", "")
    for categoria, value in categoria_config.items():
        if value == 1:
            window.categoria_combo.addItem(categoria.capitalize())

    for export_format, value in export_formats_config.items():
        if value == 1:
            window.export_combo.addItem(export_format.capitalize())
    window.show()
    sys.exit(app.exec())