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

### Preprocesamiento
Para preprocesar cada tweet, usamos la librería `nltk` (Natural Language Toolkit) de Python. Para cada archivo con tweets, generamos los tokens, eliminamos los tokens de la lista de stopwords y finalmente aplicamos `STEMMING`, con el fin de  tomar únicamente la raíz de cada palabra.

Cabe resaltar que este preprocesamiento es clave para construir un índice invertido eficiente y relevante. Además, hallando las raíces de los términos nuestra búsqueda se vuelve más precisa, abarcando así una mayor cantidad de tweets relevantes.

### Construcción del Índice Invertido

...

### Cálculo del TF-IDF

...


### Análisis del tiempo de ejecución

El tiemp de ejecución de la creación del índice invertido toma en el peor de los casos  O($t^2\cdot n$), pues para cada documento (en total $n$), se ejecuta una función cuadrática (doble for).
