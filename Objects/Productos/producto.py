class Producto:
    def __init__(self, titulo, precio):
        self.titulo = titulo
        self.precio = precio

    def __str__(self):
        return f"{self.titulo} - {self.precio}"
