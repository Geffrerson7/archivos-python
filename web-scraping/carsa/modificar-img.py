import pandas as pd

# Leer el archivo Excel
archivo_excel = "C:/Users/geffe/Desktop/codigo/silabuz-python/img-carsa.xlsx"
df = pd.read_excel(archivo_excel)

# Crear un nuevo DataFrame para almacenar los nuevos URLs
nuevos_urls_df = pd.DataFrame(columns=['SKU', 'URL'])

# Iterar sobre las filas del DataFrame original
for indice, fila in df.iterrows():
    url = fila['url']
    sku = fila['SKU']
    # Verificar si la URL termina en '-1.jpg'
    if url.endswith('-1.jpg'):
        # Generar los nuevos URLs con las modificaciones
        nuevos_urls = [url.replace('-1.jpg', f'-{i}.jpg') for i in range(2, 5)]
        # Agregar los nuevos URLs al nuevo DataFrame
        for nuevo_url in nuevos_urls:
            nuevos_urls_df = nuevos_urls_df.append({'SKU': sku, 'URL': nuevo_url}, ignore_index=True)

# Guardar los datos actualizados en un nuevo archivo Excel
nuevo_archivo_excel = "nuevos_datos_carsa.xlsx"
nuevos_urls_df.to_excel(nuevo_archivo_excel, index=False)

print(f"Se han guardado los nuevos URLs en el archivo '{nuevo_archivo_excel}'.")
