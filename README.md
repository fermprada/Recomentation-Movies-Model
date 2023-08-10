# Recomentation-Movies-Model


## Introducción


Este proyecto se enfoca en la creación de un modelo de recomendación de películas usando un dataset ya procesado y limpio. 😄

También es importante mencionar que la implementación del modelo se hace a través de una tecnología de código abierto, que permite que otras personas puedan reproducir y mejorar el modelo en el futuro. Por último, el modelo puede ser extendido a otros problemas de recomendación, como el de música o libros, ya que la metodología es muy generalizable. 😃

Este proyecto de machine learning se encuentra en la intersección de las áreas de big data, aprendizaje automático y análisis de datos. En particular, usa técnicas de preprocesado de datos, modelado, evaluación y visualización de resultados, que son temas clave en estas áreas.


A continuación una breve explicación paso a paso de lo que se hizo para llegar al producto final (Modelo de recomendación ML)


## PRIMERA PARTE: ETL


En primera instancia extraemos los dataset para trabajar en ellos, hacemos transformaciones como desanidado de diccionarios y listas, unas columnas con valores nulos se reemplazaron por 0 o fueron eliminadas, eliminamos columnas innecesarias y creamos algunas columnas según lo requerido.



## SEGUNDA PARTE: API

Para el desarrollo de la API: Se propone disponibilizar los datos usando el framework FastAPI. 

Se hicieron las siguientes consultas:

---->idioma de la película ( Idioma: str ): Se ingresa un idioma, ejemplo: (en) y te devuelve la cantidad de películas producidas en ese idioma.


---->duración de la película (Pelicula: str): Se ingresa una pelicula. Debe devolver la duracion y el año.


---->franquicia( Franquicia: str ): Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio


---->pais( Pais: str ): Se ingresa un país (como están escritos en el dataset, no hay que traducirlos!), retornando la cantidad de peliculas producidas en el mismo.


---->productoras(Productora: str ): Se ingresa la productora, entregandote el revunue total y la cantidad de peliculas que realizo.


---->director de la película (nombre_director ): Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma, en formato lista.


## TERCERA PARTE: DEPLOY



## CUARTA PARTE: EDA



## FINAL: ML MODEL
