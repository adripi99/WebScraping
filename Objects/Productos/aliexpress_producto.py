from Objects.Productos.producto import Producto

class AliexpressProducto(Producto):
    def __init__(self, titulo, precio):
        super().__init__(titulo, precio)
    def __str__(self):
        return f"{self.titulo} - {self.precio}\n"