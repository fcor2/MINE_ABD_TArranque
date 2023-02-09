from absl import flags
import sys
import bs4 as bs
import pandas as pd
import re

FLAGS = flags.FLAGS

# Flag nombre, valor por default, mensaje ayuda.
flags.DEFINE_string('archivo', None, 'Ingrese nombre archivo a procesar.')

#Lee sys.argv en FLAGS
FLAGS(sys.argv)

# Procesamiento
fname = FLAGS.archivo

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

lista_texto_procesado = genera_lista_texto(fname)
n_palabras = num_palabras(lista_texto_procesado)

print('Procesando archivo: {0}:\nTotal palabras: {1}.'.format(fname, n_palabras))


