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
df = pd.read_csv('top1000.csv')


@app.get('/peliculas_idioma/{idioma}')
async def peliculas_idioma(idioma: str):
    a = len(data[data['original_language'] == idioma])
    return {'idioma': idioma, 'cantidad': a}


'''
def peliculas_duracion( Pelicula: str ): Se ingresa una pelicula. Debe devolver la duracion y el año.
Ejemplo de retorno: X . Duración: x. Año: xx
'''

@app.get('/duracion/{pelicula}')
def peliculas_duracion(pelicula:str):
    for i, j in enumerate(data['title']):
        if j == pelicula:
            return f"Duracion: {data['runtime'][i]} minutos, año: {data['release_year'][i]}"
        else:
            continue

'''
def franquicia( Franquicia: str ): Se ingresa la franquicia, retornando la cantidad de peliculas, 
ganancia total y promedio Ejemplo de retorno: La franquicia X posee X peliculas, una ganancia 
total de x y una ganancia promedio de xx
'''
@app.get('/coleccion/{coleccion}')
def franquicia(Franquicia:str):
    collection = data[data['belongs_to_collection'] == Franquicia]
    numero = len(collection) 
    ganancia = collection['revenue'].sum()
    avg = collection['revenue'].mean()
    return f'La franquicia {Franquicia} tiene {numero} peliculas, una ganancia de {ganancia} y una ganancia promedio de {avg}'
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
@app.get('/productoras/{productora}')
def productoras_exitosas(productora:str):
    pr= data[data['produc_com1'] == productora]
    ganancia = pr['revenue'].sum()
    return (f'la productora {productora} tiene {len(pr)} peliculas y una ganancia total de {ganancia}')


'''
def get_director( nombre_director ): Se ingresa el nombre de un director 
que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido 
a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de 
lanzamiento, retorno individual, costo y ganancia de la misma, en formato lista. 
'''

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    series = data[data['name'] == nombre_director]
    retorno = series['return'].sum()
    pe= {}
    pe['name'] = nombre_director
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
with open('matriz (4).csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        data_vec.append(row)

# Convierte la lista en un arreglo NumPy
cosine = np.array(data_vec, dtype=np.float32)
indices = pd.Series(df.index, index=df['title']).drop_duplicates().to_dict()

@app.get('/recomendacion/{title}')
def recomendacion(title):
    idx = indices.get(title)
    
    if idx is None:
        return {"error": "Película no encontrada."}
    
    score = enumerate(cosine[idx])
    score = sorted(score, key=lambda x: x[1], reverse=True)
    score = score[1:6]

    sim_index = [i[0] for i in score]
    recommended_titles = df['title'].iloc[sim_index].tolist()
    return {"Peliculas recomendadas": recommended_titles}









'''
df = np.array(df).tolist()
@app.get('/recomendacion/{titulo}')
async def recomendacion(titulo:str):
    idx = data.index[data['title'] == titulo].tolist()[0]
    sim_scores = enumerate(df[idx])
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores] 
    return {'lista recomendada' : list(data['title'].iloc[movie_indices])}
'''


  