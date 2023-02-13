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

# concatena múltiples listas provenientes de n archivos

def txt_proc_agregado(lista_files):
    ''' 
    Itera función de generación de texto sobre lista de archivos
    '''
    lista_texto_procesado = list()
    
    for archivo in lista_files:
        lista_texto_procesado += genera_lista_texto(archivo)
    
    return lista_texto_procesado

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

##@app.route('/c-max_freq_palabras/int:topn>')
@app.route('/c-max_freq_palabras',methods=['POST'])
def srvcmax_freq_palabraso():
	data = request.get_json()
	fname = 'reut2-004.sgm'
	topn = data['topn']
	lista_texto_procesado = genera_lista_texto(fname)
	n_palabras = num_palabras(lista_texto_procesado)
	df = gen_df_frecuencias(lista_texto_procesado)
	ltopn = df[0:topn]
	frequencies = ltopn.to_json(orient='records')[1:-1].replace('},{', '} {')
	return jsonify(fname=fname,n_palabras=n_palabras,frequencies=frequencies)

##@app.route('/d-max_freq_palabras/<str:archivo>/<int:topn>')
@app.route('/d-max_freq_palabras',methods=['POST'])
def srvdmax_freq_palabraso():
	data = request.get_json()
	fname = data['archivo']
	topn = data['topn']
	lista_texto_procesado = genera_lista_texto(fname)
	n_palabras = num_palabras(lista_texto_procesado)
	df = gen_df_frecuencias(lista_texto_procesado)
	ltopn = df[0:topn]
	frequencies = ltopn.to_json(orient='records')[1:-1].replace('},{', '} {')
	return jsonify(fname=fname,n_palabras=n_palabras,frequencies=frequencies)


##@app.route('/e-dos_max_freq_palabras/<str:listaarchivos>/<int:topn>/<int:flagsinrank>')
@app.route('/e-dos_max_freq_palabras',methods=['POST'])
def srve_dosmax_freq_palabraso():
	data = request.get_json()
	listafname = data['listaarchivos']
	listafiles = listafname.split("|")
	topn = data['topn']
	flagsinrank = data['flagsinrank']

	lista_texto_procesado = txt_proc_agregado(listafiles)
	n_palabras = num_palabras(lista_texto_procesado)
	df = gen_df_frecuencias(lista_texto_procesado)
	
    #Selecciona el top m de palabras más frecuentes
	if flagsinrank == 1:
		ltopn = df[0:topn]
		frequencies = ltopn.to_json(orient='records')[1:-1].replace('},{', '} {')
	else:
		frequencies = df.to_json(orient='records')[1:-1].replace('},{', '} {')
	return jsonify(fname=listafname,n_palabras=n_palabras,frequencies=frequencies)

##@app.route('/f-n_max_freq_palabras/<str:listaarchivos>/<int:topn>/<int:flagsinrank>')
@app.route('/f-n_max_freq_palabras',methods=['POST'])
def srvf_n_max_freq_palabraso():
	data = request.get_json()
	listafname = data['listaarchivos']
	listafiles = listafname.split("|")
	topn = data['topn']
	flagsinrank = data['flagsinrank']

	lista_texto_procesado = txt_proc_agregado(listafiles)
	n_palabras = num_palabras(lista_texto_procesado)
	df = gen_df_frecuencias(lista_texto_procesado)
	
    #Selecciona el top m de palabras más frecuentes
	if flagsinrank == 1:
		ltopn = df[0:topn]
		frequencies = ltopn.to_json(orient='records')[1:-1].replace('},{', '} {')
	else:
		frequencies = df.to_json(orient='records')[1:-1].replace('},{', '} {')
	return jsonify(fname=listafname,n_palabras=n_palabras,frequencies=frequencies)


if __name__ == '__main__':
    app.run(debug=True, port=8090)
