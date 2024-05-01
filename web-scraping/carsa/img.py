import os
import requests
import pandas as pd

def descargar_imagen(url, ruta_guardado):
    try:
        # Realizar la solicitud GET a la URL de la imagen
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Construir el nombre del archivo
            nombre_archivo = os.path.join(ruta_guardado, os.path.basename(url))
            # Guardar la imagen en el archivo
            with open(nombre_archivo, 'wb') as archivo:
                for chunk in response.iter_content(1024):
                    archivo.write(chunk)
            print(f"La imagen {nombre_archivo} ha sido descargada correctamente.")
        else:
            print(f"No se pudo descargar la imagen desde {url}. Código de estado HTTP: {response.status_code}")
    except Exception as e:
        print(f"Ocurrió un error al descargar la imagen desde {url}: {str(e)}")

# Leer el archivo Excel
archivo_excel = "C:/Users/geffe/Desktop/codigo/silabuz-python/img-carsa.xlsx"
df = pd.read_excel(archivo_excel)

# Ruta donde se guardarán las imágenes descargadas
ruta_guardado = "C:/Users/geffe/Documents/SILABUZ/carsa/full-img"

# Verificar si la ruta de guardado existe, si no, crearla
if not os.path.exists(ruta_guardado):
    os.makedirs(ruta_guardado)

# Iterar sobre las filas del DataFrame
for indice, fila in df.iterrows():
    url = fila['url']
    # Verificar si la URL termina en '-1' o '-2', '-3', '-4'
    if url.endswith('-1.jpg') or url.endswith('-2.jpg') or url.endswith('-3.jpg') or url.endswith('-4.jpg'):
        # Descargar la imagen
        descargar_imagen(url, ruta_guardado)

print("Todas las imágenes han sido descargadas y guardadas en la ruta especificada.")
