
from Objects.Web.aliexpress_web import AliexpressWeb
from Objects.Web.amazon_web import AmazonWeb
from Objects.Productos.coleccion_productos import ColeccionProductos
from datetime import datetime
import os
web="Amazon"
categoria = "electrónica"
num_productos = 5
atributos_en_profundidad = True
show_browser = True
running = True
log_callback = None
export_format="csv"
atributos_a_extraer=["Review"]

if web == "Amazon":
    web = AmazonWeb(show_browser)
elif web == "Aliexpress":
    web = AliexpressWeb(show_browser)

productos = web.buscar_productos(categoria,num_productos,atributos_en_profundidad,atributos_a_extraer,log_callback)



