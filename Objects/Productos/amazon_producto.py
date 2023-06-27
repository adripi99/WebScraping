from Objects.Productos.producto import Producto

class AmazonProducto(Producto):
    def __init__(self, titulo, precio, asin, review=None, vendedor=None, estrellas=None):
        super().__init__(titulo, precio)
        self.asin = asin
        self.review=review
        self.vendedor=vendedor
        self.estrellas=estrellas
    def __str__(self):
        return f"{self.titulo} - {self.precio} - {self.asin}\n"