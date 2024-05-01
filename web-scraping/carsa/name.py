import pandas as pd
import json

# Listas para almacenar los datos de los productos
todos_nombres = []
todas_marcas = []
todos_skus = []
todos_img = []

# Iterar sobre los nombres de los archivos JSON
for i in range(1, 6):
    nombre_archivo = f"C:/Users/geffe/Desktop/codigo/silabuz-python/web-scraping/carsa/data-{i}.json"
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        # Carga los datos del archivo JSON en una variable de Python
        productos = json.load(archivo)
        
        # Iterar sobre los productos y extraer los nombres, marcas y SKUs
        for producto in productos:
            image_url= producto.get("image_url", "")
            marca = producto.get("marca", "")
            sku = producto.get("sku", "")
            nombre = producto.get("name", "")
            todas_marcas.append(marca)
            todos_skus.append(sku)
            todos_nombres.append(nombre)
            todos_img.append(image_url)

# Crear un DataFrame de pandas con los datos
df = pd.DataFrame({"Nombre de Producto": todos_nombres,
                   "Marca": todas_marcas,
                   "SKU": todos_skus,
                   "Image URL": todos_img})

# Guardar los datos en un archivo Excel
archivo_excel = "datos-carsa.xlsx"
df.to_excel(archivo_excel, index=False)

print(f"Se han guardado los datos de los productos en el archivo '{archivo_excel}'.")

