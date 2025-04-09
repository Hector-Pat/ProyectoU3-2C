"""
Detector de Plagio para Trabajos Estudiantiles
Versión integrada (todas las funciones en un solo archivo)
"""

import os
import re
import time
from datetime import datetime

# ===== PREPROCESAMIENTO DE TEXTO =====

def clean_text(text):
    """Limpia el texto eliminando signos de puntuación y convirtiendo a minúsculas"""
    # Convertir a minúsculas
    cleaned_text = text.lower()
    
    # Eliminar signos de puntuación y caracteres especiales
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)
    
    # Eliminar números
    cleaned_text = re.sub(r'\d+', '', cleaned_text)
    
    # Eliminar espacios múltiples
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    return cleaned_text

def generate_ngrams(text, n=3):
    """Divide el texto en n-gramas"""
    words = text.split(' ')
    ngrams = []
    
    # Si hay menos palabras que el tamaño del n-grama, devolver una lista vacía
    if len(words) < n:
        return ngrams
    
    # Generar n-gramas
    for i in range(len(words) - n + 1):
        ngram = ' '.join(words[i:i+n])
        ngrams.append(ngram)
    
    return ngrams

def load_document(file_path):
    """Carga un documento desde un archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error al cargar el documento {file_path}: {e}")
        return ''

def load_documents_from_directory(dir_path):
    """Carga todos los documentos de un directorio"""
    documents = {}
    
    try:
        files = os.listdir(dir_path)
        
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(dir_path, file)
                documents[file] = load_document(file_path)
        
        return documents
    except Exception as e:
        print(f"Error al cargar documentos del directorio: {e}")
        return {}

def preprocess_document(text, n=3):
    """Preprocesa un documento: lo limpia y genera n-gramas"""
    cleaned_text = clean_text(text)
    return generate_ngrams(cleaned_text, n)

# ===== TABLA HASH =====

def custom_hash(string, table_size):
    """Función hash personalizada para cadenas de texto"""
    hash_value = 0
    PRIME = 31
    
    for char in string:
        hash_value = (hash_value * PRIME + ord(char)) % table_size
    
    return hash_value

class HashTable:
    """Implementación de una tabla hash con manejo de colisiones por encadenamiento"""
    
    def __init__(self, size=1024):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0
    
    def insert(self, key, value):
        """Inserta un elemento en la tabla hash"""
        index = custom_hash(key, self.size)
        
        # Buscar si la clave ya existe
        bucket = self.table[index]
        for i, item in enumerate(bucket):
            if item[0] == key:
                # Si la clave existe, actualizar el valor
                if value not in item[1]:
                    item[1].append(value)
                return
        
        # Si la clave no existe, agregarla
        bucket.append([key, [value]])
        self.count += 1
        
        # Verificar si es necesario redimensionar la tabla
        if self.count > self.size * 0.7:
            self._resize(self.size * 2)
    
    def search(self, key):
        """Busca un elemento en la tabla hash"""
        index = custom_hash(key, self.size)
        
        bucket = self.table[index]
        for item in bucket:
            if item[0] == key:
                return item[1]
        
        return None
    
    def _resize(self, new_size):
        """Redimensiona la tabla hash"""
        old_table = self.table
        self.size = new_size
        self.table = [[] for _ in range(new_size)]
        self.count = 0
        
        # Reinserta todos los elementos
        for bucket in old_table:
            for key, values in bucket:
                for value in values:
                    self.insert(key, value)

# ===== FILTRO DE BLOOM =====

class BloomFilter:
    """Implementación de un filtro de Bloom"""
    
    def __init__(self, size=10000, hash_count=3):
        self.size = size
        self.hash_count = hash_count
        # Crear un array de bits (representado como un array de booleanos)
        self.bit_array = [False] * size
    
    def add(self, item):
        """Agrega un elemento al filtro"""
        # Aplicar cada función hash y marcar los bits correspondientes
        for index in self._get_hash_values(item):
            self.bit_array[index] = True
    
    def contains(self, item):
        """Verifica si un elemento podría estar en el filtro"""
        # Verificar si todos los bits correspondientes están marcados
        return all(self.bit_array[index] for index in self._get_hash_values(item))
    
    def _get_hash_values(self, item):
        """Obtiene los índices hash para un elemento"""
        indices = []
        
        # Usar las funciones hash disponibles
        if self.hash_count >= 1:
            indices.append(self._hash1(item))
        if self.hash_count >= 2:
            indices.append(self._hash2(item))
        if self.hash_count >= 3:
            indices.append(self._hash3(item))
        
        return indices
    
    def _hash1(self, string):
        """Función hash 1"""
        hash_value = 0
        for char in string:
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value
    
    def _hash2(self, string):
        """Función hash 2"""
        hash_value = 0
        for char in string:
            hash_value = (hash_value * 37 + ord(char)) % self.size
        return hash_value
    
    def _hash3(self, string):
        """Función hash 3"""
        hash_value = 0
        for char in string:
            hash_value = (hash_value * 17 + ord(char)) % self.size
        return hash_value

# ===== CÁLCULO DE SIMILITUD =====

def jaccard_similarity(set_a, set_b):
    """Calcula la similitud de Jaccard entre dos conjuntos"""
    # Si ambos conjuntos están vacíos, la similitud es 1
    if len(set_a) == 0 and len(set_b) == 0:
        return 1
    
    # Calcular la intersección
    intersection = set_a.intersection(set_b)
    
    # Calcular la unión
    union = set_a.union(set_b)
    
    # Calcular el coeficiente de Jaccard
    return len(intersection) / len(union)

def document_similarity(ngrams_a, ngrams_b):
    """Calcula la similitud entre dos documentos basada en sus n-gramas"""
    set_a = set(ngrams_a)
    set_b = set(ngrams_b)
    
    return jaccard_similarity(set_a, set_b)

def calculate_similarity_matrix(documents_ngrams):
    """Calcula la matriz de similitud entre múltiples documentos"""
    document_names = list(documents_ngrams.keys())
    similarity_matrix = []
    
    # Comparar cada par de documentos
    for i in range(len(document_names)):
        doc_a = document_names[i]
        ngrams_a = documents_ngrams[doc_a]
        
        for j in range(i + 1, len(document_names)):
            doc_b = document_names[j]
            ngrams_b = documents_ngrams[doc_b]
            
            similarity = document_similarity(ngrams_a, ngrams_b)
            
            similarity_matrix.append({
                'doc_a': doc_a,
                'doc_b': doc_b,
                'similarity': similarity
            })
    
    return similarity_matrix

# ===== ALGORITMO DE ORDENAMIENTO =====

def merge_sort(arr, key=None, ascending=False):
    """Función principal de Merge Sort"""
    # Caso base: una lista con 0 o 1 elementos ya está ordenada
    if len(arr) <= 1:
        return arr
    
    # Dividir la lista en dos mitades
    middle = len(arr) // 2
    left = arr[:middle]
    right = arr[middle:]
    
    # Ordenar recursivamente ambas mitades
    return merge(
        merge_sort(left, key, ascending),
        merge_sort(right, key, ascending),
        key,
        ascending
    )

def merge(left, right, key, ascending):
    """Función para combinar dos listas ordenadas"""
    result = []
    left_index = 0
    right_index = 0
    
    # Comparar elementos de ambas listas y combinarlos en orden
    while left_index < len(left) and right_index < len(right):
        left_value = left[left_index][key] if key else left[left_index]
        right_value = right[right_index][key] if key else right[right_index]
        
        # Determinar el orden según el parámetro ascending
        if ascending:
            should_take_left = left_value <= right_value
        else:
            should_take_left = left_value >= right_value
        
        if should_take_left:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1
    
    # Agregar los elementos restantes
    return result + left[left_index:] + right[right_index:]

def get_top_similar_pairs(similarity_matrix, n=10):
    """Ordena los resultados de similitud y devuelve los N pares más similares"""
    # Ordenar por similitud en orden descendente
    sorted_matrix = merge_sort(similarity_matrix, 'similarity', False)
    
    # Devolver los N primeros pares
    return sorted_matrix[:n]

# ===== VISUALIZACIÓN =====

def generate_ascii_graph(similarity_pairs, threshold=0.3):
    """Genera una representación en texto ASCII de un grafo de similitud"""
    # Filtrar pares por umbral de similitud
    filtered_pairs = [pair for pair in similarity_pairs if pair['similarity'] >= threshold]
    
    # Obtener todos los documentos únicos
    documents = set()
    for pair in filtered_pairs:
        documents.add(pair['doc_a'])
        documents.add(pair['doc_b'])
    
    doc_array = sorted(list(documents))
    
    # Crear matriz de adyacencia
    adjacency_matrix = {}
    for doc in doc_array:
        adjacency_matrix[doc] = {}
        for other_doc in doc_array:
            adjacency_matrix[doc][other_doc] = 0
    
    # Llenar matriz de adyacencia con valores de similitud
    for pair in filtered_pairs:
        adjacency_matrix[pair['doc_a']][pair['doc_b']] = pair['similarity']
        adjacency_matrix[pair['doc_b']][pair['doc_a']] = pair['similarity']
    
    # Generar representación ASCII
    graph = f"Grafo de Similitud (umbral: {threshold})\n"
    graph += "================================\n\n"
    
    for doc in doc_array:
        graph += f"{doc} -->\n"
        
        # Mostrar conexiones
        has_connections = False
        for other_doc in doc_array:
            if doc != other_doc and adjacency_matrix[doc][other_doc] >= threshold:
                similarity = adjacency_matrix[doc][other_doc] * 100
                connection_strength = get_connection_strength(adjacency_matrix[doc][other_doc])
                graph += f"   {connection_strength} {other_doc} ({similarity:.2f}%)\n"
                has_connections = True
        
        if not has_connections:
            graph += "   (sin conexiones significativas)\n"
        
        graph += "\n"
    
    return graph

def get_connection_strength(similarity):
    """Genera una representación visual de la fuerza de conexión"""
    if similarity >= 0.8:
        return "====>"
    if similarity >= 0.6:
        return "===>"
    if similarity >= 0.4:
        return "==>"
    return "=>"

def generate_similarity_table(similarity_pairs):
    """Genera una tabla de similitud en formato de texto"""
    # Ordenar pares por similitud (de mayor a menor)
    sorted_pairs = sorted(similarity_pairs, key=lambda x: x['similarity'], reverse=True)
    
    # Generar encabezado de la tabla
    table = "Tabla de Similitud entre Documentos\n"
    table += "=================================\n\n"
    table += "| Documento A      | Documento B      | Similitud (%) |\n"
    table += "|------------------|------------------|---------------|\n"
    
    # Generar filas de la tabla
    for pair in sorted_pairs:
        doc_a = pair['doc_a'].ljust(18)
        doc_b = pair['doc_b'].ljust(18)
        similarity = f"{pair['similarity'] * 100:.2f}".rjust(13)
        
        table += f"| {doc_a}| {doc_b}| {similarity} |\n"
    
    return table

# ===== FUNCIÓN PRINCIPAL =====

def detect_plagiarism(documents_dir='./documentos', ngram_size=3, top_n=10, similarity_threshold=0.3):
    """Función principal del detector de plagio"""
    print("=== Detector de Plagio para Trabajos Estudiantiles ===\n")
    print(f"Analizando documentos en: {documents_dir}")
    print(f"Tamaño de n-gramas: {ngram_size}")
    
    # Paso 1: Cargar documentos
    print("\nCargando documentos...")
    start_time = time.time()
    documents = load_documents_from_directory(documents_dir)
    document_count = len(documents)
    
    if document_count == 0:
        print("No se encontraron documentos para analizar.")
        return
    
    print(f"Se cargaron {document_count} documentos en {time.time() - start_time:.2f} segundos.")
    
    # Paso 2: Preprocesar documentos y generar n-gramas
    print("\nPreprocesando documentos y generando n-gramas...")
    start_time = time.time()
    documents_ngrams = {}
    hash_table = HashTable()
    bloom_filter = BloomFilter(100000, 3)
    
    # Para cada documento, preprocesar y generar n-gramas
    for doc_name, content in documents.items():
        ngrams = preprocess_document(content, ngram_size)
        documents_ngrams[doc_name] = ngrams
        
        # Paso 3: Almacenar n-gramas en la tabla hash y filtro de Bloom
        for ngram in ngrams:
            hash_table.insert(ngram, doc_name)
            bloom_filter.add(ngram)
        
        print(f"  - {doc_name}: {len(ngrams)} n-gramas generados")
    
    print(f"Preprocesamiento completado en {time.time() - start_time:.2f} segundos.")
    
    # Paso 4: Calcular similitud entre documentos
    print("\nCalculando similitud entre documentos...")
    start_time = time.time()
    similarity_matrix = calculate_similarity_matrix(documents_ngrams)
    print(f"Cálculo de similitud completado en {time.time() - start_time:.2f} segundos.")
    
    # Paso 5: Ordenar resultados usando Merge Sort
    print("\nOrdenando resultados...")
    start_time = time.time()
    top_similar_pairs = get_top_similar_pairs(similarity_matrix, top_n)
    print(f"Ordenamiento completado en {time.time() - start_time:.2f} segundos.")
    
    # Paso 6: Mostrar los N pares más similares
    print(f"\nTop {top_n} pares de documentos más similares:")
    print(generate_similarity_table(top_similar_pairs))
    
    # Visualización adicional: grafo de similitud
    print("\nGrafo de similitud entre documentos:")
    print(generate_ascii_graph(top_similar_pairs, similarity_threshold))
    
    # Guardar resultados en un archivo
    results_dir = './resultados'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    results_file = os.path.join(results_dir, f"resultados_{timestamp}.txt")
    
    results = "=== RESULTADOS DEL DETECTOR DE PLAGIO ===\n\n"
    results += f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    results += f"Documentos analizados: {document_count}\n"
    results += f"Tamaño de n-gramas: {ngram_size}\n\n"
    results += generate_similarity_table(top_similar_pairs)
    results += "\n\n"
    results += generate_ascii_graph(top_similar_pairs, similarity_threshold)
    
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write(results)
    
    print(f"\nResultados guardados en: {results_file}")

# ===== EJECUCIÓN PRINCIPAL =====

if __name__ == "__main__":
    import sys
    
    # Obtener argumentos de la línea de comandos
    documents_dir = sys.argv[1] if len(sys.argv) > 1 else './documentos'
    ngram_size = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    top_n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    similarity_threshold = float(sys.argv[4]) if len(sys.argv) > 4 else 0.3
    
    detect_plagiarism(documents_dir, ngram_size, top_n, similarity_threshold)