# importa librerias
import bs4 as bs
import pandas as pd
import re
import sys

# nombre del archivo
fname = 'reut2-021.sgm'

# genera el objeto 'Soup'
f = open(fname, 'r')
data = f.read()
soup = bs.BeautifulSoup(data, 'html.parser')

def captura_textos(soup):
    
    '''--------------------------
    Recibe objeto soup para cada archivo de reuters.
    Genera lista de títulos y de cuerpos para cada artículo.
    Existen títulos sin cuerpo.
    '''
    
    lista_art, lista_titulos = list(), list()
    
    for art in soup.find_all('body'):
        lista_art.append(art.get_text())
    
    for art in soup.find_all('title'):
        lista_titulos.append(art.get_text())
    
    lista_texto = lista_art + lista_titulos
    
    return lista_texto

def adecuacion_texto(ls):
    '''--------------------------
    Recibe lista de distintos strings.
    '''
    nueva_lista = list()
    for texto in ls:
        minusculas = texto.lower()
        sin_puntuacion = re.sub(r'[^\w\s][^\\n]', '', minusculas)
        nueva_lista.append(sin_puntuacion)
    return nueva_lista

def num_palabras(ls):
    count = 0
    for texto in ls:
        for palabra in texto.split():
            count += 1
    return count

def gen_df_frecuencias(ls):
    '''
    ------------------------
    Recibe lista agregada de texto y genera diccionario en formato {palabra: frecuencia}
    '''
    d = dict()
    for texto in ls:
        for word in texto.split():
            if word in d:
                d[word] += 1
            else:
                d[word] = 1
    flag_index = [i for i in range(len(d))]
    df = pd.DataFrame.from_dict(data = d, orient='index')
    df['Palabras'] = df.index.values
    df['indx'] = flag_index
    df['Freq'] = df[0]
    df.set_index(['indx'], inplace=True)
    df = df[['Palabras', 'Freq']]
    df_s = df.sort_values(by='Freq', ascending=False).reset_index()
    df_s = df_s[['Palabras', 'Freq']]
    return df_s

# Corre funciones con 1 archivo

lista_texto = captura_textos(soup)
lista_texto_limpia = adecuacion_texto(lista_texto)

n_palabras = num_palabras(lista_texto_limpia)

print('Archivo: {0}:\n{1} Número total de palabras.'.format(fname, n_palabras))
print('(Sólo incluye cuerpos y títulos).\n')

# genera tabla de grecuentcias
df = gen_df_frecuencias(lista_texto_limpia)

print(df.head(30))
