import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QComboBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from Web.amazon_web import AmazonWeb
from Productos.coleccion_productos import ColeccionProductos

class Worker(QThread):
    finished = pyqtSignal()

    def __init__(self, url, num_paginas, export_format):
        super().__init__()
        self.url = url
        self.num_paginas = num_paginas
        self.export_format = export_format
        self.running = True
    def run(self):
        # obtener los productos
        driver_path = "C:/Users/adrip/Desktop/VSC/Seleniumtfg2023/Objects/chromedriver.exe"
        web = AmazonWeb(driver_path)
        productos = web.buscar_productos(self.url, self.num_paginas)
        # exportar los productos
        if self.export_format == "JSON":
            productos.exportar_json("productos.json")
        elif self.export_format == "CSV":
            productos.exportar_csv("productos.csv")
        elif self.export_format == "Pandas":
            productos.exportar_pandas()

        self.finished.emit()
    def stop(self):
        self.running = False
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = None

        self.setWindowTitle("Amazon Web Scraper")
        self.setGeometry(100, 100, 400, 200)

        self.url_label = QLabel("URL:")
        self.url_edit = QLineEdit()

        self.num_paginas_label = QLabel("Número de páginas:")
        self.num_paginas_edit = QLineEdit()

        self.export_label = QLabel("Formato de exportación:")
        self.export_combo = QComboBox()
        self.export_combo.addItem("JSON")
        self.export_combo.addItem("CSV")
        self.export_combo.addItem("Pandas")

        self.start_button = QPushButton("Iniciar")

        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_edit)
        layout.addWidget(self.num_paginas_label)
        layout.addWidget(self.num_paginas_edit)
        layout.addWidget(self.export_label)
        layout.addWidget(self.export_combo)
        layout.addWidget(self.start_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.start_button.clicked.connect(self.start_scraping)

    def start_scraping(self):
        if self.worker is not None and self.worker.isRunning(): #me aseguro del hilo
            self.worker.stop() 
        url = self.url_edit.text()
        num_paginas = int(self.num_paginas_edit.text())
        export_format = self.export_combo.currentText()

        self.worker = Worker(url, num_paginas, export_format)
        self.worker.start() #esperar al hilo principal revisar error QThread: Destroyed while thread is still running

    def scraping_finished(self):
        self.statusBar().showMessage("Scraping finalizado")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())