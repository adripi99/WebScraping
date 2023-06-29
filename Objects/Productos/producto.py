class Producto:
    def __init__(self, titulo, precio):
        self.Titulo = titulo
        self.Precio = precio

    def __str__(self):
        return f"{self.Titulo} - {self.Precio}"
