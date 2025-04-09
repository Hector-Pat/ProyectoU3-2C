# Punto de entrada principal del detector de plagio
"""
Detector de Plagio para Trabajos Estudiantiles
Programa principal que integra todos los componentes
"""

import os
import time
from datetime import datetime
from src.utils.preprocessing import preprocess_document, load_documents_from_directory
from src.hash.hash_table import HashTable
from src.hash.bloom_filter import BloomFilter
from src.similarity.jaccard import calculate_similarity_matrix
from src.sorting.merge_sort import get_top_similar_pairs
from src.visualization.graph import generate_ascii_graph, generate_similarity_table

def detect_plagiarism(documents_dir=r"C:\Users\ferne\OneDrive\Documentos\100Archivos\archivos", ngram_size=3, top_n=10, similarity_threshold=0.3):
    """
    Función principal del detector de plagio
    
    Args:
        documents_dir (str): Directorio con los documentos a analizar
        ngram_size (int): Tamaño de los n-gramas
        top_n (int): Número de pares más similares a mostrar
        similarity_threshold (float): Umbral de similitud para el grafo
    """
    print("=== Detector de Plagio para Trabajos Estudiantiles ===\n")
    print(f"Analizando documentos en: {documents_dir}")
    print(f"Tamaño de n-gramas: {ngram_size}")
    
    # Paso 1: Cargar documentos
    print("\nCargando documentos...")
    documents = load_documents_from_directory(documents_dir)
    document_count = len(documents)
    
    if document_count == 0:
        print("No se encontraron documentos para analizar.")
        return
    
    print(f"Se cargaron {document_count} documentos.")
    
    # Paso 2: Preprocesar documentos y generar n-gramas
    print("\nPreprocesando documentos y generando n-gramas...")
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
    
    # Paso 4: Calcular similitud entre documentos
    print("\nCalculando similitud entre documentos...")
    similarity_matrix = calculate_similarity_matrix(documents_ngrams)
    
    # Paso 5: Ordenar resultados usando Merge Sort
    print("\nOrdenando resultados...")
    top_similar_pairs = get_top_similar_pairs(similarity_matrix, top_n)
    
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

if __name__ == "__main__":
    import sys
    
    # Obtener argumentos de la línea de comandos
    documents_dir = sys.argv[1] if len(sys.argv) > 1 else './documentos'
    ngram_size = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    top_n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    similarity_threshold = float(sys.argv[4]) if len(sys.argv) > 4 else 0.3
    
    detect_plagiarism(documents_dir, ngram_size, top_n, similarity_threshold)