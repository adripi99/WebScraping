class TripadvisorProducto:
    """
    Clase que representa un producto de Tripadvisor.

    Args:
        nombre (str): Nombre del producto.
        direccion (str): Dirección del producto.
        telefono (str): Teléfono del producto.
        opiniones (str): Número de opiniones del producto.

    Attributes:
        Nombre (str): Nombre del producto.
        Direccion (str): Dirección del producto.
        Telefono (str): Teléfono del producto.
        Opiniones (str): Número de opiniones del producto.

    """

    def __init__(self, nombre, direccion, telefono, opiniones):
        self.Nombre = nombre
        self.Direccion = direccion
        self.Telefono = telefono
        self.Opiniones = opiniones

    def __str__(self):
        return f"{self.Nombre} - {self.Direccion} - Teléfono: {self.Telefono} - Opiniones: {self.Opiniones}"
