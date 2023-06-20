from Web.amazon_web import AmazonWeb
from Productos.coleccion_productos import ColeccionProductos

web = AmazonWeb()
categoria = "ordenadores"
num_productos = 20
productos = web.buscar_productos(categoria, num_productos)
for index, row in productos.df.iterrows():
    titulo = row['titulo']
    precio = row['precio']
    asin = row['asin']
    ruta = row['ruta']
    print(titulo, precio, asin, ruta)
web.cerrar_navegador