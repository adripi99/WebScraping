from Objects.Productos.producto import Producto

class AliexpressProducto(Producto):
    def __init__(self, Titulo, Precio,Estrellas=None, Vendedor=None):
        super().__init__(Titulo, Precio)
        self.Estrellas=Estrellas
        self.Vendedor=Vendedor
    def __str__(self):
        return f"{self.Titulo} - {self.Precio}\n"