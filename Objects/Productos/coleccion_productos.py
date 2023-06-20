import pandas as pd

class ColeccionProductos:
    def __init__(self,lista_seleccion):
        self.df = pd.DataFrame(columns=lista_seleccion)  #paso la lista de seleccion del user
        #self.df = pd.DataFrame(columns=["titulo", "precio", "asin", "ruta"])
       
    def agregar_producto(self, producto):
         nuevo_df = pd.DataFrame([producto.__dict__])
         self.df = pd.concat([self.df, nuevo_df], ignore_index=True)


    def eliminar_duplicados(self):
        self.df = self.df.drop_duplicates()

    def exportar(self, formato, path):
        archivo = path.split("/")[-1]
        ruta = "/".join(path.split("/")[:-1]) + "/"
        
        if formato == "json":
            json_data = self.df.to_json(orient="records", indent=4)
            with open(path, "w") as f:
                f.write(json_data)
        elif formato == "csv":
            self.df.to_csv(path, index=False)
        elif formato == "excel":
            self.df.to_excel(path, index=False)
        elif formato == "html":
            self.df.to_html(path, index=False)
        elif formato == "pickle":
            self.df.to_pickle(path)
        elif formato == "parquet":
            self.df.to_parquet(path)
        elif formato == "feather":
            self.df.to_feather(path)
        elif formato == "hdf":
            self.df.to_hdf(path, key="data", mode="w")
        else:
            raise ValueError("Formato de exportación no válido.")