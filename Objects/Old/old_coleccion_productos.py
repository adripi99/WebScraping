import pandas as pd
import json
import csv

class ColeccionProductos:
    def __init__(self):
        self.productos = []
        #pasar a data frame y despues exportar al formato que se quere
    def __iter__(self):
        return iter(self.productos)
    
    def agregar_producto(self, producto):
        if producto not in self.productos:
            self.productos.append(producto)

    def eliminar_duplicados(self):
        self.productos = list(set(self.productos))

    def exportar_json(self, archivo):
        with open(archivo, "w") as f:
            json.dump([p.__dict__ for p in self.productos], f, indent=4)

    def exportar_csv(self, archivo):
        with open(archivo, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["titulo", "precio", "asin"])
            for p in self.productos:
                writer.writerow([p.titulo, p.precio, p.asin])

    def exportar_pandas(self):
        data = [(p.titulo, p.precio, p.asin) for p in self.productos]
        df = pd.DataFrame(data, columns=["titulo", "precio", "asin"])
        df.to
        return df