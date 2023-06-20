from Objects.Productos.producto import Producto

class AmazonProducto(Producto):
    def __init__(self, titulo, precio, asin):
        super().__init__(titulo, precio)
        self.asin = asin
    def __str__(self):
        return f"{self.titulo} - {self.precio} - {self.asin}\n"