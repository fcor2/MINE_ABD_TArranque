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

# genera lista de listas de texto procesado, una para cada archivo
def txt_proc_individual(lista_files):
    ''' 
    Genera una lista para cada archivo de texto procesado
    '''
    ls_ls_texto_archivo = list()
    
    for archivo in lista_files:
        ls_ls_texto_archivo.append(genera_lista_texto(archivo))
    
    return ls_ls_texto_archivo

# Devuelve el nombre del archivo con mayor # de palabras y el conteo
def get_max(dict,lista_files):
    '''
    Compara el número de palabras de cada archivo.
    Retorna el nombre de archivo con mayor número de palabras
    y el conteo.
    Retorna <nombre archivo>, <conteo>
    '''
    conteo_max = 0
    arch_grande = str()
    for archivo in lista_files:
        conteo_arch = dict.get(archivo)
        if conteo_arch > conteo_max:
            conteo_max = conteo_arch
            arch_grande = archivo
    
    return arch_grande, conteo_max

#Genera lista con df correspondiente a cada archivo
def get_df_ls_archivo(ls_ls_texto_archivo):
    '''
    Genera lista de dataframes [df1, df2,..., dfn]
    Cada df contiene tabla de frecuencias ordenada
    de mayor a menor cols: ['Palabras', 'Freq']
    '''
    ls_df = list()
    
    for ls_tx in ls_ls_texto_archivo:
        ls_df.append(gen_df_frecuencias(ls_tx))
    
    return ls_df


#Encuentra frecuencias de palabras en df
def encuentra_freq_palabra(df, palabra_clave):
    '''
    Retorna la frecuencia de la palabra clave 
    en el dataframe
    '''
    freq = df.loc[df['Palabras'] == palabra_clave].Freq.values[0]
    return freq

#Compara freq de palabra clave en lista de df
def dict_freq_palabra(ls_df, palabra_clave,lista_files):
    
    dict_f_palabra = dict()
    i = 0
    
    for df in ls_df:
        freq = encuentra_freq_palabra(df, palabra_clave)
        dict_f_palabra[lista_files[i]] = freq
        i += 1
    
    return dict_f_palabra

# Diccionario para conteo de palabras
def dict_conteo(ls_ls_texto_archivo,listafiles):
    '''
    Genera un diccionario: {<archivo>, valor}
    donde valor es el num total de palabras
    '''
    dict_conteo = dict()
    i = 0
    
    for ls in ls_ls_texto_archivo:
        n_palabras = num_palabras(ls)
        dict_conteo[listafiles[i]] = n_palabras
        i += 1
    
    return dict_conteo

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

##@app.route('/g-busqueda_arch_palabra/<str:listaarchivos>/<str:palabra_clave>')
@app.route('/g-busqueda_arch_palabra',methods=['POST'])
def srvg_n_busqueda_arch_palabra():
	data = request.get_json()
	listafname = data['listaarchivos']
	listafiles = listafname.split("|")
	palabra_clave = data['palabra_clave']

	ls_ls_texto_archivo = txt_proc_individual(listafiles)
	dict_conteo_var = dict_conteo(ls_ls_texto_archivo,listafiles)
	arch_grande, conteo_max = get_max(dict_conteo_var,listafiles)
	ls_df = get_df_ls_archivo(ls_ls_texto_archivo)
	d_frecuencias = dict_freq_palabra(ls_df, palabra_clave,listafiles)
	arch_mas_freq, frequenc = get_max(d_frecuencias,listafiles)

	return jsonify(listafname=listafname,arch_grande=arch_grande,conteo_max=int(conteo_max),arch_mas_freq=arch_mas_freq,palabra_clave=palabra_clave,freq=int(frequenc))


if __name__ == '__main__':
	app.run(debug=True, port=8090)



