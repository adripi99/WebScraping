#!TFG\Scripts\python.exe
import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from utils import load_config

if __name__ == "__main__":
    app = QApplication(sys.argv)
    jsondata= load_config("Vista_config.json") #encoding utf
    window = MainWindow(jsondata)
    window.cambia_categoria()
    window.show()
    try:
        sys.exit(app.exec())
    except Exception as e:
        print("Se produjo un error:", str(e))