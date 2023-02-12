from absl import flags
import sys
import bs4 as bs
import pandas as pd
import re
from flask import Flask, request,jsonify
app = Flask(__name__)


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

##@app.route('/a-num_palabras/<str:archivo>')
@app.route('/a-num_palabras',methods=['POST'])
def srvnum_palabras():
	data = request.get_json()
	fname = data['archivo']
	lista_texto_procesado = genera_lista_texto(fname)
	n_palabras = num_palabras(lista_texto_procesado)
	return jsonify(fname=fname,n_palabras=n_palabras)


##@app.route('/b-freq_palabras/<str:archivo>')
@app.route('/b-freq_palabras',methods=['POST'])
def srvfreq_palabraso():
	data = request.get_json()
	fname = data['archivo']
	lista_texto_procesado = genera_lista_texto(fname)
	n_palabras = num_palabras(lista_texto_procesado)
	df = gen_df_frecuencias(lista_texto_procesado)
	frequencies = df.to_json(orient='records')[1:-1].replace('},{', '} {')
	return jsonify(fname=fname,n_palabras=n_palabras,frequencies=frequencies)

if __name__ == '__main__':
    app.run(debug=True, port=8090)
