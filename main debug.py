
from Objects.Web.aliexpress_web import AliexpressWeb
from Objects.Web.amazon_web import AmazonWeb
from Objects.Productos.coleccion_productos import ColeccionProductos
from datetime import datetime
web="Amazon"
categoria = "moda"
num_productos = 70
atributos_en_profundidad = False
show_browser = False
running = True
log_callback = None
export_format="csv"
atributos_a_extraer=["Titulo","Precio"]

if web == "Amazon":
    web = AmazonWeb(show_browser)
elif web == "Aliexpress":
    web = AliexpressWeb(show_browser)

productos = web.buscar_productos(categoria,num_productos,atributos_en_profundidad,atributos_a_extraer,log_callback)
# exportar los 
productos.exportar(export_format,"C:/Users/adrip/Desktop/VSC/Seleniumtfg2023/Objects/Export/"+datetime.now().strftime('%Y-%m-%d')+"."+export_format)


