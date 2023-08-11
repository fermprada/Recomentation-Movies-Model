import pandas as pd
import numpy as np
from typing import Union
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI
import csv

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


data = pd.read_csv('df_f.csv')
df = pd.read_csv('demo_ movies.csv')


@app.get('/peliculas_idioma/{idioma}')
async def peliculas_idioma(idioma: str):
    a = len(data[data['original_language'] == idioma])
    return {'idioma': idioma, 'cantidad': a}


'''
def peliculas_duracion( Pelicula: str ): Se ingresa una pelicula. Debe devolver la duracion y el año.
Ejemplo de retorno: X . Duración: x. Año: xx
'''
@app.get('/peliculas_duracion/{pelicula}')
async def peliculas_duracion(pelicula):
    d = data[['runtime', 'release_year']][data['title'] == pelicula]
    duracion = int(d['runtime'][1])
    anio = int(d['release_year'][1])
    return {'pelicula':pelicula, 'duracion':f'{duracion}min', 'anio':anio}


'''
def franquicia( Franquicia: str ): Se ingresa la franquicia, retornando la cantidad de peliculas, 
ganancia total y promedio Ejemplo de retorno: La franquicia X posee X peliculas, una ganancia 
total de x y una ganancia promedio de xx
'''
@app.get('/franquicia/{franquicia}')
async def franquicia(franquicia: str):
    collection = data[data['belongs_to_collection'] == franquicia]
    numero = len(collection) 
    ganacia = collection['revenue'].sum()
    promedio = collection['revenue'].mean()
    return {'franquicia':franquicia, 'cantidad':numero, 'ganancia_total':ganacia, 'ganancia_promedio':promedio}

'''
def peliculas_pais( Pais: str ): Se ingresa un país (como están escritos en el dataset, 
no hay que traducirlos!), retornando la cantidad de peliculas producidas en el mismo.
Ejemplo de retorno: Se produjeron X películas en el país X
'''

@app.get('/peliculas_pais/{pais}')
async def peliculas_pais(pais: str):
    collection = data[data['country'] == pais]
    num = len(collection)
    return {'pais':pais, 'cantidad':num}

'''
def productoras_exitosas( Productora: str ): Se ingresa la productora, 
entregandote el revunue total y la cantidad de peliculas que realizo.
Ejemplo de retorno: La productora X ha tenido un revenue de x 
'''

@app.get('/productoras_exitosas/{Productora}')
async def productoras_exitosas(Productora: str):
    collection = data[data['pro_comp1'] == Productora]
    num = len(collection)
    revenue = collection['revenue'].sum()
    return {'productora':Productora, 'revenue_total': revenue,'cantidad':num}

'''
def get_director( nombre_director ): Se ingresa el nombre de un director 
que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido 
a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de 
lanzamiento, retorno individual, costo y ganancia de la misma, en formato lista. 
'''

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    series = df[df['director'] == nombre_director]
    retorno = series['return'].sum()
    pe= {}
    pe['director'] = nombre_director
    pe['retorno total'] = retorno
 
    peliculas = []

    for i in range(int(len(series))):
        peli = {}
        peli['titulo'] = series['title'].iloc[i]
        peli['fecha de estreno'] = str(series['release_date'].iloc[i])
        peli['retorno'] = str(series['return'].iloc[i])
        peli['presupuesto'] = str(series['budget'].iloc[i])
        peli['ganancia'] = series['revenue'].iloc[i]
        peliculas.append(peli)
    pe['peliculas'] = peliculas
    return pe
'''
 return {'director':nombre_director, 'retorno_total_director':respuesta, 
    'peliculas':respuesta, 'anio':respuesta,, 'retorno_pelicula':respuesta, 
    'budget_pelicula':respuesta, 'revenue_pelicula':respuesta}
'''
# ML

'''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''


data_vec = []
with open('baseline_vec_df.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        data_vec.append(row)

# Convierte la lista en un arreglo NumPy
cosine = np.array(data_vec, dtype=np.float32)
indices = pd.Series(df.index, index=df['title']).drop_duplicates().to_dict()

@app.get('/recomendacion/{title}')
def recomendacion(title):

    score = sorted(score, key=lambda x: x[1], reverse=True)
    score = score[1:6]

    sim_index = [i[0] for i in score]
    recommended_titles = df['title'].iloc[sim_index].tolist()
    return {"recommended_movies": recommended_titles}