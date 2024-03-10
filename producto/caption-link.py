import pandas as pd

# Función para realizar los reemplazos y convertir a minúsculas
def reemplazar_y_convertir(texto):
    texto = texto.replace(' ', '-')  # Reemplazar espacios en blanco por guiones
    texto = texto.replace('+', '')  # Eliminar el símbolo '+'
    return texto.lower()  # Convertir a minúsculas

# Cargar el archivo Excel
archivo_excel = "mi_archivo.xlsx"
df = pd.read_excel(archivo_excel)

# Aplicar la función reemplazar_y_convertir a todas las columnas
df = df.applymap(reemplazar_y_convertir)

# Guardar el DataFrame modificado en un nuevo archivo Excel
archivo_nuevo = "caption-link.xlsx"
df.to_excel(archivo_nuevo, index=False)

print("¡Proceso completado!")
