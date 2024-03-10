import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Descarga los recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Carga el archivo Excel
df = pd.read_excel('nombre-gef.xlsx')

# Selecciona la columna de interés
columna_interes = 'Nombre'

# Función para identificar sustantivos
def identificar_sustantivos(texto):
    tokens = word_tokenize(texto)
    etiquetados = pos_tag(tokens)
    sustantivos = [palabra.lower() for palabra, etiqueta in etiquetados if etiqueta.startswith('NN') and palabra.lower() not in ['de', 'para', 'y', 'con', 'sin', 'en', 'más']]
    return ', '.join(sustantivos)


# Aplica la función a la columna seleccionada
df['sustantivos'] = df[columna_interes].apply(identificar_sustantivos)

# Guarda el resultado en un nuevo archivo Excel
df.to_excel('keywords-venuts-1.xlsx', index=False)
