import pandas as pd

# Lee el archivo Excel
df = pd.read_excel("C:/Users/geffe/Desktop/lista-nombres-suntime.xlsx")

# Supongamos que la columna con los nombres de los productos se llama 'Producto'
# Extrae el SKU usando una expresión lambda
df['SKU'] = df['Producto'].apply(lambda x: x.split(' - ')[1] if ' - ' in x else '')

# Guarda el DataFrame con los SKU extraídos en un nuevo archivo Excel
df.to_excel('C:/Users/geffe/Desktop/lista-SKU-suntime.xlsx', index=False)

