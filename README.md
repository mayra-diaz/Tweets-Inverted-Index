# Proyecto 2 - Organización de Archivos

**Curso: Base de datos II**
**Profesor: Heider Sánchez**
**Integrantes:**
- Joaquín Elías Ramírez Gutiérrez 201910277
- Paolo André Morey Tutiven 201910236
- Mayra Díaz Tramontana 201910147

## Introducción

### Objetivo del proyecto
- Entender y aplicar algoritmos de búsqueda y recuperación de la información basada en el contenido.
- Implementar una estructura óptima de índica invertido de tipo Block-Sorted para tareas de búsqueda y recuperación de la información en documentos de texto



### Descripción del dominio de datos a usar
Para este proyecto hemos utilizado data de [Kaggle](https://onedrive.live.com/?authkey=%21ANNEKv7tNdlSSQk&id=C2923DF9F1F816F%2150804&cid=0C2923DF9F1F816F). Esta data representa un conjunto de miles de Tweets, en los cuales se realizarán las búsquedas e inserciones. Es una cantidad atinada de tuplas para realizar todas nuestras pruebas, validaciones, test y experimentos, pues refleja una cantidad masiva de información manejada en el mundo real.




## Funcionamiento

Con `index.add('./test/')` se añaden todos los archivos de la carpeta 'test' al índice. Y con `index.analyze_query(query, n)`
se analiza el string query y retorna los n tweets más parecidos.

### Preprocesamiento
Para preprocesar cada tweet, usamos la librería `nltk` (Natural Language Toolkit) de Python. Para cada archivo con tweets, generamos los tokens, eliminamos los tokens de la lista de stopwords y finalmente aplicamos `STEMMING`, con el fin de  tomar únicamente la raíz de cada palabra.

Cabe resaltar que este preprocesamiento es clave para construir un índice invertido eficiente y relevante. Además, hallando las raíces de los términos nuestra búsqueda se vuelve más precisa, abarcando así una mayor cantidad de tweets relevantes.

### Construcción del Índice Invertido
Se construye y almacena el índice invertido utilizando una metadata con información necesaria. El índice tiene un tamaño de bloque 100,
cada bloque se almacena en un archivo distinto. Además, para poder encontrar los tweets, se almacena en un archivo ordenado su id, 
por lo tanto sabemos donde está ubicado en n*log(n). 

El índice tiene la estructura:
```json
{
  "apag": {
    "tf": 1,
    "tweets": {
      "1027663142447448070": {
        "tdf": 1,
        "w": 1.2429372745195837
      }
    },
    "df": 1
  },
  "apagon": {
    "tf": 1,
    "tweets": {
      "1027359295862710273": {
        "tdf": 1,
        "w": 1.2429372745195837
      }
    },
    "df": 1
  },
  ...
}
```

### Cálculo del TF-IDF
El índice almacena el tdf, tf y idf, por lo tanto, cada vez que añadimos tweets volvemos a calcular los pesos.


### Análisis del tiempo de ejecución

El tiemp de ejecución de la creación del índice invertido toma en el peor de los casos  O($t^2\cdot n$), pues para cada documento (en total $n$), se ejecuta una función cuadrática (doble for).
