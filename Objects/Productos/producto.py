class Producto:
    """
    Clase Producto que representa un producto con un título y un precio.

    Args:
        titulo (str): Título del producto.
        precio (float): Precio del producto.

    """
    def __init__(self, titulo, precio):
        """
        Inicializa una instancia de la clase Producto con el título y el precio especificados.

        Args:
            titulo (str): Título del producto.
            precio (float): Precio del producto.

        """
        self.Titulo = titulo
        self.Precio = precio

    def __str__(self):
        """
        Devuelve una representación en cadena del producto.

        Returns:
            str: Representación en cadena del producto en formato "Título - Precio".

        """
        return f"{self.Titulo} - {self.Precio}"
