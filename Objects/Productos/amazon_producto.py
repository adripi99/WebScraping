from Objects.Productos.producto import Producto

class AmazonProducto(Producto):
    def __init__(self, Titulo, Precio, Asin, Review=None, Vendedor=None, Estrellas=None):
        super().__init__(Titulo, Precio)
        self.Asin = Asin
        self.Review=Review
        self.Vendedor=Vendedor
        self.Estrellas=Estrellas
    def __str__(self):
        return f"{self.Titulo} - {self.Precio} - {self.Asin}\n"