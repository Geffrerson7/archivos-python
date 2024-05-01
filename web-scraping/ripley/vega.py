import unicodedata
import requests, json
import pandas as pd

# Cargar el archivo Excel
df = pd.read_excel("C:/Users/geffe/Desktop/codigo/silabuz-python/nombres-sku-vega.xlsx")

# Función para eliminar tildes
def eliminar_tildes(texto):
    return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))

# Aplicar función para eliminar tildes y reemplazar comas por guiones en la columna 'nombre'
df["nombre"] = df["nombre"].apply(lambda x: eliminar_tildes(x.lower()).replace(" ", "-").replace(",", "-"))

# Concatenar 'nombre' y 'sku' separados por '-'
df["resultado"] = df["nombre"] + "-" + df["sku"].astype(str).apply(lambda x: x.split("-")[0])

# Convertir el resultado a una lista
resultado_lista = df["resultado"].tolist()
descriptions_list = []

for nombre, sku in zip(df["resultado"], df["sku"].astype(str).apply(lambda x: x.split("-")[0])):
    url = (
        "https://www.vega.pe/_v/segment/routing/vtex.store@2.x/product/"
        + str(sku)
        + "/"
        + nombre
        + "/p?__pickRuntime=appsEtag%2Cblocks%2CblocksTree%2Ccomponents%2CcontentMap%2Cextensions%2Cmessages%2Cpage%2Cpages%2Cquery%2CqueryData%2Croute%2CruntimeMeta%2Csettings&__device=tablet"
    )
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Si hay un error en la solicitud, lanzar una excepción
        data = response.json()
        # Acceder al primer elemento de data["queryData"]
        query_data = data["queryData"][0]

        # Decodificar el JSON contenido en la cadena de la clave "data"
        product_data = json.loads(query_data["data"])

        # Obtener la descripción del producto
        product_description = product_data["product"]["items"][0]["images"]["imageUrl"]
        print(product_description)
        descriptions_list.append(product_description)
    except requests.exceptions.HTTPError as err:
        print(f"Error HTTP al obtener la descripción para SKU {sku}: {err}")
        descriptions_list.append("")  # Agregar una cadena vacía en caso de error

df_description = pd.DataFrame({"Description": descriptions_list})
df_description.to_excel("vega-descripcion.xlsx", index=False)

print("¡Proceso completado!")
