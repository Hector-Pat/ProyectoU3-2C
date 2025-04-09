import os

# Crear la estructura de directorios
directories = [
    'documentos',
    'resultados',
    'src',
    'src/utils',
    'src/hash',
    'src/similarity',
    'src/sorting',
    'src/visualization',
    'tests'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Directorio creado: {directory}")

# Crear archivos base
files = [
    {'path': 'src/__init__.py', 'content': '# Paquete detector de plagio\n'},
    {'path': 'src/utils/__init__.py', 'content': '# Paquete de utilidades\n'},
    {'path': 'src/hash/__init__.py', 'content': '# Paquete de funciones hash\n'},
    {'path': 'src/similarity/__init__.py', 'content': '# Paquete de cálculo de similitud\n'},
    {'path': 'src/sorting/__init__.py', 'content': '# Paquete de algoritmos de ordenamiento\n'},
    {'path': 'src/visualization/__init__.py', 'content': '# Paquete de visualización\n'},
    {'path': 'src/utils/preprocessing.py', 'content': '# Funciones para preprocesamiento de texto\n'},
    {'path': 'src/hash/hash_table.py', 'content': '# Implementación de tabla hash\n'},
    {'path': 'src/hash/bloom_filter.py', 'content': '# Implementación de filtro de Bloom\n'},
    {'path': 'src/similarity/jaccard.py', 'content': '# Cálculo de similitud de Jaccard\n'},
    {'path': 'src/sorting/merge_sort.py', 'content': '# Implementación del algoritmo Merge Sort\n'},
    {'path': 'src/visualization/graph.py', 'content': '# Visualización de resultados\n'},
    {'path': 'src/main.py', 'content': '# Punto de entrada principal del detector de plagio\n'},
    {'path': 'README.md', 'content': '# Detector de Plagio para Trabajos Estudiantiles\n\n## Descripción\n\nSistema de detección de plagio que identifica similitudes entre trabajos estudiantiles.\n'}
]

for file in files:
    with open(file['path'], 'w', encoding='utf-8') as f:
        f.write(file['content'])
    print(f"Archivo creado: {file['path']}")

print('Estructura del proyecto creada exitosamente.')