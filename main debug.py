
from Objects.Web.aliexpress_web import AliexpressWeb
from Objects.Web.amazon_web import AmazonWeb
from Objects.Web.tripadvisor_web import TripadvisorWeb
from Objects.Productos.coleccion_productos import ColeccionProductos
from datetime import datetime
web="Tripadvisor"
categoria = "Gijon"
num_productos = 2
atributos_en_profundidad = True
show_browser = True
running = True
log_callback = None
export_format="csv"
atributos_a_extraer=["Nombre"]

if web == "Amazon":
    web = AmazonWeb(show_browser)
elif web == "Aliexpress":
    web = AliexpressWeb(show_browser)
elif web == "Tripadvisor":
    web = TripadvisorWeb(show_browser)

productos = web.buscar_productos(categoria,num_productos,atributos_en_profundidad,atributos_a_extraer,log_callback)
# exportar los 
productos.exportar(export_format,"C:/Users/adrip/Desktop/VSC/Seleniumtfg2023/Objects/Export/"+datetime.now().strftime('%Y-%m-%d')+"."+export_format)


