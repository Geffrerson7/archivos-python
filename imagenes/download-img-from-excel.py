import pandas as pd
import requests
import os
from PIL import Image
from io import BytesIO
from PIL import ImageOps


# Función para descargar y procesar una imagen
def procesar_imagen(url, sku, carpeta_destino):
    """Función para descargar y procesar una imagen."""
    # Reemplazar "," por "|"
    url = url.replace(",", "|")
    # Reemplazar "%7C" por "|"
    url = url.replace("%7C", "|")
    # Dividir los enlaces por los separadores "|"
    enlaces_separados = url.split("|")

    for i, enlace in enumerate(enlaces_separados, start=1):
        nombre_archivo = f"{sku}-{i}.jpg"  # Nombre del archivo será SKU-i.jpg
        ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)  # Ruta completa del archivo

        try:
            respuesta = requests.get(enlace.strip())  # Eliminar espacios en blanco
            if respuesta.ok:
                imagen = Image.open(BytesIO(respuesta.content))
                imagen = imagen.convert("RGB")  # Convertir la imagen a formato RGB

                # Redimensionar la imagen manteniendo su relación de aspecto original
                max_dimension = 1000
                ancho, alto = imagen.size
                proporcion = max_dimension / max(ancho, alto)
                nuevo_ancho = round(ancho * proporcion)
                nuevo_alto = round(alto * proporcion)
                imagen = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

                # Crear un lienzo blanco de 1000x1000 píxeles y pegar la imagen en el centro
                lienzo = Image.new("RGB", (max_dimension, max_dimension), color="white")
                posicion_x = (max_dimension - nuevo_ancho) // 2
                posicion_y = (max_dimension - nuevo_alto) // 2
                lienzo.paste(imagen, (posicion_x, posicion_y))

                lienzo.save(ruta_archivo, "JPEG", quality=95)  # Guardar la imagen en formato JPEG
                print(f"Imagen guardada: {ruta_archivo}")
            else:
                print(f"Error al descargar la imagen {enlace}: {respuesta.status_code}")
        except Exception as e:
            print(f"Error al procesar la imagen {enlace}: {e}")


# Cargar el archivo Excel
archivo_excel = "primera-carga-vultec.xlsx"
df = pd.read_excel(archivo_excel)

# Carpeta donde se guardarán las imágenes
carpeta_destino = "C:/Users/geffe/Desktop/codigo/PRODUCT-SCRAPING/vultec-img-primera"
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# List to store SKUs with empty image links
skus_sin_imagen = []

# Iterar sobre las filas del DataFrame
for index, fila in df.iterrows():
    enlaces_imagen = fila["url"]
    sku = fila["SKU"]
    if pd.isna(enlaces_imagen) or enlaces_imagen.strip() == "":
        skus_sin_imagen.append(sku)
    else:
        procesar_imagen(enlaces_imagen, sku, carpeta_destino)

# Guardar los SKUs sin imagen en un nuevo archivo Excel
df_sin_imagen = pd.DataFrame({"SKU": skus_sin_imagen})
df_sin_imagen.to_excel("skus_sin_imagen.xlsx", index=False)

print("¡Proceso completado!")
