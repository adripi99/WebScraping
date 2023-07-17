from PyQt6.QtWidgets import QMainWindow, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QComboBox, QTextEdit, QCheckBox, QListWidget, QMessageBox
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from worker import Worker
class MainWindow(QMainWindow):
    """
    Clase MainWindow que representa la interfaz de usuario principal.

    """
    def __init__(self,json):
        super().__init__()
        self.jsondata=json
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
        self.log_text.setReadOnly(True)
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
    def Merror(self,error_text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Error")
        msg.setInformativeText(error_text)
        msg.setWindowTitle("Error")
        msg.exec()
    def start_scraping(self):
        """
        Inicia el proceso de web scraping con los parámetros especificados.

        """
        if self.worker is not None and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()
            self.worker.deleteLater()

        web = self.web_combo.currentText()
        categoria = self.categoria_combo.currentText()
        num_productos_text = self.num_productos_edit.text()
        export_format = self.export_combo.currentText().lower()
        show_browser = self.show_browser_checkbox.isChecked()
        atributos_a_extraer = [self.selected_products_list.item(i).text() for i in range(self.selected_products_list.count())]
        atributos_en_profundidad= False

        if any(atributo in atributos_a_extraer for atributo, valor in self.jsondata[web].get("atributos", {}).items() if valor == 1):
            atributos_en_profundidad = True

        try:
            num_productos = int(num_productos_text)
            if num_productos <= 0:
                self.Merror("El número de productos debe ser mayor a cero.")
                return
        except ValueError:
            self.Merror("Ingrese un número válido para el número de productos.")
            return
        
        if not atributos_a_extraer:
            self.Merror("Debe seleccionar al menos un atributo para extraer.")
            return
        
        self.start_button.setEnabled(False)  # Deshabilitar el botón de inicio
        self.log_callback("Comenzando el Scraping, espere.")

        self.worker = Worker(web, categoria, num_productos, atributos_a_extraer, atributos_en_profundidad, show_browser,export_format, self.log_callback)

        self.worker.finished.connect(self.scraping_finished)

        self.worker.start()
       
    def cambia_categoria(self):
        """
        Actualiza la lista de categorías disponibles según la página web seleccionada.

        """
        config = self.jsondata
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
        self.worker = None

    def log_callback(self, message):
        """
        Agrega un mensaje al registro de eventos en la interfaz de usuario.

        Args:
            message (str): Mensaje a agregar al registro.

        """
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum()) # Asegura que el texto agregado esté visible en la parte inferior del QTextEdit
