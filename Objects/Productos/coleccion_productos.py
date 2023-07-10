import pandas as pd

class ColeccionProductos:
    """
    Clase ColeccionProductos que representa una colección de productos y proporciona funcionalidades como agregar productos, eliminar duplicados y exportar los datos en diferentes formatos.

    Args:
        lista_seleccion (list): Lista de columnas seleccionadas para la colección de productos.

    """
    def __init__(self,lista_seleccion):
        """
        Inicializa una instancia de la clase ColeccionProductos con la lista de selección especificada.

        Args:
            lista_seleccion (list): Lista de columnas seleccionadas para la colección de productos.

        """
        self.df = pd.DataFrame(columns=lista_seleccion)  #paso la lista de seleccion del user
        self.seleccion=lista_seleccion
       
    def agregar_producto(self, producto):
         """
        Agrega un producto a la colección.

        Args:
            producto (Producto): Producto a agregar a la colección.

        """
         nuevo_df = pd.DataFrame([producto.__dict__])
         self.df = pd.concat([self.df, nuevo_df], ignore_index=True)

    #Exportar al final de extraer los datos, recorrer en 2 niveles todos los produtos. Usar un dict en amazon web
    def eliminar_duplicados(self):
        """
        Elimina los productos duplicados de la colección.

        """
        self.df = self.df.drop_duplicates()

    def exportar(self, formato, path):
        """
        Exporta los datos de la colección en el formato especificado.

        Args:
            formato (str): Formato de exportación ("json", "csv", "html", "pickle", "parquet", "feather", "hdf").
            path (str): Ruta de archivo para guardar los datos exportados.

        Raises:
            ValueError: Si se proporciona un formato de exportación no válido.

        """
        df_seleccionado = self.df[self.seleccion]
        if formato == "json":
            json_data = df_seleccionado.to_json(orient="records", indent=4)
            with open(path, "w") as f:
                f.write(json_data)
        elif formato == "csv":
            df_seleccionado.to_csv(path, index=False)
        elif formato == "html":
            df_seleccionado.to_html(path, index=False)
        elif formato == "pickle":
            df_seleccionado.to_pickle(path)
        elif formato == "parquet":
            df_seleccionado.to_parquet(path)
        elif formato == "feather":
            df_seleccionado.to_feather(path)
        elif formato == "hdf":
            df_seleccionado.to_hdf(path, key="data", mode="w")
        else:
            raise ValueError("Formato de exportación no válido.")