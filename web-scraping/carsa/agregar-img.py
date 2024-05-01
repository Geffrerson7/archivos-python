import pandas as pd

# Cargar el archivo Excel
archivo_excel = "C:/Users/geffe/Desktop/codigo/silabuz-python/img-carsa.xlsx"
datos = pd.read_excel(archivo_excel)

# Iterar sobre cada fila del DataFrame
for index, row in datos.iterrows():
    url = row['url']
    if url.endswith("-1.jpg"):
        # Construir los nuevos URLs
        nuevo_url_1 = url.replace("-1.jpg", "-2.jpg")
        nuevo_url_2 = url.replace("-1.jpg", "-3.jpg")
        nuevo_url_3 = url.replace("-1.jpg", "-4.jpg")
        
        # Modificar la fila con los nuevos URLs
        datos.at[index, 'url'] = f"{url},{nuevo_url_1},{nuevo_url_2},{nuevo_url_3}"

# Guardar los datos modificados en un nuevo archivo Excel
nuevo_archivo_excel = "datos_modificados_carsa.xlsx"
datos.to_excel(nuevo_archivo_excel, index=False)

print("Proceso completado. Los datos modificados se han guardado en un nuevo archivo Excel.")
