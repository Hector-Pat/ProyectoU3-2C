# Detector de Plagio para Trabajos Estudiantiles

## Descripción

### Detector de Plagio para Trabajos Estudiantiles

## Descripción general del proyecto

Este sistema detecta similitudes entre trabajos estudiantiles (archivos de texto plano) utilizando tablas hash para el almacenamiento y comparación eficiente de datos textuales, y algoritmos de ordenamiento para clasificar los documentos según su similitud.

El detector de plagio funciona mediante los siguientes pasos:

1. Tokeniza cada documento en secuencias (n-gramas)
2. Utiliza funciones hash para mapear los n-gramas en tablas hash y filtros de Bloom
3. Compara los valores hash para detectar similitudes usando el coeficiente de Jaccard
4. Clasifica las puntuaciones de similitud utilizando el algoritmo Merge Sort
5. Muestra los N pares de documentos más similares


## Instrucciones de instalación y ejecución

### Requisitos previos

- Python 3.6 o superior


### Instalación

1. Clonar el repositorio:


```shellscript
https://github.com/Hector-Pat/ProyectoU3-2C.git
cd ProyectoU3-2C.git
```

2. Instalar dependencias (si es necesario):


```shellscript
pip install -r requirements.txt
```

### Ejecución

Existen dos formas de ejecutar el detector de plagio:

#### Opción 1: Usando el script integrado (recomendado)

1. Asegúrate de que tus documentos .txt estén en una carpeta específica.
2. Edita el archivo `ejecutar_detector_integrado.py` y actualiza la variable `documents_dir` con la ruta a tu carpeta de documentos:


```python
documents_dir = r"C:\ruta\a\tus\documentos"  # Actualiza esta ruta
```

3. Ejecuta el script:


```shellscript
python ejecutar_detector_integrado.py
```

#### Opción 2: Ejecutando directamente el módulo principal

```shellscript
python detector_plagio.py "C:\ruta\a\tus\documentos" 3 20 0.3
```

Donde:

- `"C:\ruta\a\tus\documentos"`: Ruta a la carpeta con los documentos
- `3`: Tamaño de los n-gramas
- `20`: Número de pares más similares a mostrar
- `0.3`: Umbral de similitud para el grafo


## Ejemplo de uso

### Paso 1: Preparar los documentos

Coloca los archivos de texto (.txt) que deseas analizar en una carpeta específica, por ejemplo: `C:\Users\usuario\Documentos\trabajos_estudiantes`

### Paso 2: Ejecutar el detector

```shellscript
python ejecutar_detector_integrado.py
```

### Paso 3: Revisar los resultados

Los resultados se mostrarán en la consola y también se guardarán en un archivo de texto en la carpeta `resultados/` con un nombre que incluye la fecha y hora del análisis.

## Estructura del proyecto

```plaintext
detector-plagio/
├── documentos/           # Carpeta para los documentos a analizar
├── resultados/           # Carpeta donde se guardan los resultados
├── src/                  # Código fuente modular del proyecto
│   ├── hash/
│   │   ├── __init__.py
│   │   ├── bloom_filter.py  # Implementación del filtro de Bloom
│   │   └── hash_table.py    # Implementación de la tabla hash
│   ├── similarity/
│   │   ├── __init__.py
│   │   └── jaccard.py      # Cálculo de similitud de Jaccard
│   ├── sorting/
│   │   ├── __init__.py
│   │   └── merge_sort.py    # Implementación del algoritmo Merge Sort
│   ├── utils/
│   │   ├── __init__.py
│   │   └── preprocessing.py # Preprocesamiento de texto
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── graph.py        # Visualización de resultados
│   ├── __init__.py
│   └── main.py           # Punto de entrada principal
├── tests/                # Casos de prueba y archivos de prueba
├── detector_plagio.py    # Versión integrada (todas las funciones en un solo archivo)
├── ejecutar_detector_integrado.py  # Script para ejecutar el detector integrado
├── requirements.txt      # Lista de dependencias
└── README.md             # Este archivo
```

## Componentes principales

### 1. Preprocesamiento de texto (`src/utils/preprocessing.py`)

- **Funcionalidad**: Limpieza y tokenización de documentos
- **Funciones principales**:

- `clean_text()`: Elimina signos de puntuación y convierte a minúsculas
- `generate_ngrams()`: Divide el texto en secuencias de n palabras consecutivas
- `load_documents_from_directory()`: Carga todos los documentos de un directorio
- `preprocess_document()`: Combina limpieza y generación de n-gramas





### 2. Tabla Hash (`src/hash/hash_table.py`)

- **Funcionalidad**: Almacenamiento eficiente de n-gramas
- **Características**:

- Implementación personalizada de tabla hash
- Función hash personalizada para cadenas de texto
- Manejo de colisiones por encadenamiento
- Redimensionamiento automático





### 3. Filtro de Bloom (`src/hash/bloom_filter.py`)

- **Funcionalidad**: Optimización de memoria para verificar presencia de n-gramas
- **Características**:

- Estructura de datos probabilística
- Múltiples funciones hash
- Verificación rápida de pertenencia





### 4. Cálculo de similitud (`src/similarity/jaccard.py`)

- **Funcionalidad**: Cálculo de similitud entre documentos
- **Algoritmo**: Coeficiente de Jaccard

- Fórmula: J(A,B) = |A ∩ B| / |A ∪ B|
- Donde A y B son conjuntos de n-gramas de dos documentos
- El resultado es un valor entre 0 (sin similitud) y 1 (idénticos)





### 5. Algoritmo de ordenamiento (`src/sorting/merge_sort.py`)

- **Funcionalidad**: Ordenamiento eficiente de los resultados de similitud
- **Algoritmo**: Merge Sort

- Complejidad temporal: O(n log n)
- Estable y eficiente para grandes conjuntos de datos





### 6. Visualización (`src/visualization/graph.py`)

- **Funcionalidad**: Presentación visual de los resultados
- **Formatos**:

- Tabla de similitud: Muestra pares de documentos ordenados por similitud
- Grafo ASCII: Representa visualmente las conexiones entre documentos similares





## Flujo de ejecución

1. **Carga de documentos**: El sistema carga todos los archivos .txt de la carpeta especificada.
2. **Preprocesamiento**: Cada documento es limpiado (eliminación de signos de puntuación, conversión a minúsculas) y dividido en n-gramas.
3. **Indexación**: Los n-gramas se almacenan en una tabla hash y un filtro de Bloom para búsquedas eficientes.
4. **Cálculo de similitud**: Se calcula la similitud de Jaccard entre cada par de documentos.
5. **Ordenamiento**: Los pares de documentos se ordenan según su similitud utilizando Merge Sort.
6. **Visualización**: Se muestran los N pares más similares en formato de tabla y grafo.
7. **Almacenamiento**: Los resultados se guardan en un archivo de texto en la carpeta `resultados/`.


## Optimizaciones implementadas

1. **Tabla Hash**: Permite búsquedas de n-gramas en tiempo constante O(1) en promedio.
2. **Filtro de Bloom**: Reduce el uso de memoria al verificar rápidamente si un n-grama podría estar presente.
3. **Merge Sort**: Algoritmo de ordenamiento eficiente con complejidad O(n log n).
4. **Procesamiento por lotes**: Los documentos se procesan de manera eficiente para manejar grandes volúmenes.


## Resultados

Los resultados del análisis se presentan en dos formatos:

### 1. Tabla de similitud

Muestra los pares de documentos ordenados por su grado de similitud:

```plaintext
Tabla de Similitud entre Documentos
=================================

| Documento A      | Documento B      | Similitud (%) |
|------------------|------------------|---------------|
| doc1.txt         | doc5.txt         |         85.75 |
| doc2.txt         | doc3.txt         |         72.30 |
...
```

### 2. Grafo de similitud

Representa visualmente las conexiones entre documentos similares:

```plaintext
Grafo de Similitud (umbral: 0.3)
================================

doc1.txt -->
   ====> doc5.txt (85.75%)
   ===> doc2.txt (65.20%)

doc2.txt -->
   ====> doc3.txt (72.30%)
   ...
```

## Instrucciones para replicar resultados

Para replicar los resultados del análisis:

1. Asegúrate de tener la misma colección de documentos en la carpeta especificada.
2. Utiliza los mismos parámetros:

1. Tamaño de n-gramas: 3 (tri-gramas)
2. Número de pares a mostrar: 20
3. Umbral de similitud: 0.3



3. Ejecuta el detector con el mismo comando:


```shellscript
python ejecutar_detector_integrado.py
```

4. Los resultados deberían ser idénticos, salvo pequeñas variaciones en los tiempos de ejecución.


## Rendimiento

El sistema está optimizado para manejar grandes conjuntos de documentos (100+) mediante:

- Uso eficiente de tablas hash para búsquedas rápidas
- Filtros de Bloom para reducir el uso de memoria
- Algoritmo Merge Sort para ordenamiento eficiente


En pruebas con 100 documentos, el sistema completa el análisis en pocos segundos, dependiendo del hardware.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.

## Autores

Hector Pat Sosa
Lilia Contreras
Fernely Flores
Angel Ortiz

---

*Proyecto desarrollado para el Instituto Tecnológico de Software (CCT 31PSU0097H)*
