from absl import flags
import sys
import bs4 as bs
import pandas as pd
import re

FLAGS = flags.FLAGS

# Flag nombre, valor por default, mensaje ayuda.
# se llama usando --archivo=<nombre_de_archivo1,<nombre_de_archivo2>
flags.DEFINE_string('archivos', None, 'Ingrese los nombres de los archivos a procesar, separados por ",".')

# se llama usando --n=<int>
# Flag que recibe 'n' para calcular n-palabras más frecuentes
#flags.DEFINE_integer('n', 1, 'Ingrese nombre archivo a procesar.')

#Lee sys.argv en FLAGS
FLAGS(sys.argv)

# Procesamiento
string_archivos = FLAGS.archivos
lista_files = string_archivos.split(",")
#fname = FLAGS.archivo
#top_n = FLAGS.n


def genera_lista_texto(fname):
    '''----------------------
    Genera objeto soup
    '''
    f = open(fname, 'r')
    data = f.read()
    soup = bs.BeautifulSoup(data, 'html.parser')

    '''----------------------
    Recibe objeto soup y genera lista agregada 
    de títulos y cuerpos.
    '''
    lista_art, lista_titulos = list(), list()
    
    for art in soup.find_all('body'):
        lista_art.append(art.get_text())
    
    for art in soup.find_all('title'):
        lista_titulos.append(art.get_text())
    
    lista_texto = lista_art + lista_titulos
    
    '''--------------------------
    Recibe lista de texto y adecua para conteo/procesamiento.
    Formato en minúsculas
    Elimina puntuación
    '''
    nueva_lista = list()
    for texto in lista_texto:
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

# concatena múltiples listas provenientes de n archivos

def txt_proc_agregado(lista_files):
    ''' 
    Itera función de generación de texto sobre lista de archivos
    '''
    lista_texto_procesado = list()
    
    for archivo in lista_files:
        lista_texto_procesado += genera_lista_texto(archivo)
    
    return lista_texto_procesado

lista_texto_procesado = txt_proc_agregado(lista_files)

n_palabras = num_palabras(lista_texto_procesado)
print('Procesando archivo(s): {0}:\nTotal palabras: {1}.'.format(lista_files, n_palabras))