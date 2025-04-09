"""
Módulo para calcular la similitud entre documentos usando el coeficiente de Jaccard
"""

def jaccard_similarity(set_a, set_b):
    """
    Calcula la similitud de Jaccard entre dos conjuntos
    Fórmula: J(A,B) = |A ∩ B| / |A ∪ B|
    
    Args:
        set_a (set): Primer conjunto
        set_b (set): Segundo conjunto
        
    Returns:
        float: Coeficiente de Jaccard (entre 0 y 1)
    """
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
    """
    Calcula la similitud entre dos documentos basada en sus n-gramas
    
    Args:
        ngrams_a (list): N-gramas del primer documento
        ngrams_b (list): N-gramas del segundo documento
        
    Returns:
        float: Similitud entre los documentos (entre 0 y 1)
    """
    set_a = set(ngrams_a)
    set_b = set(ngrams_b)
    
    return jaccard_similarity(set_a, set_b)

def calculate_similarity_matrix(documents_ngrams):
    """
    Calcula la matriz de similitud entre múltiples documentos
    
    Args:
        documents_ngrams (dict): Diccionario con nombres de documentos como claves y listas de n-gramas como valores
        
    Returns:
        list: Lista de diccionarios con pares de documentos y su similitud
    """
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

# Ejemplo de uso
if __name__ == "__main__":
    set_a = {'a', 'b', 'c', 'd'}
    set_b = {'c', 'd', 'e', 'f'}
    
    print("Similitud de Jaccard entre conjuntos:", jaccard_similarity(set_a, set_b))
    
    ngrams_a = ['este es un', 'es un ejemplo', 'un ejemplo de']
    ngrams_b = ['es un ejemplo', 'un ejemplo de', 'ejemplo de texto']
    
    print("Similitud entre documentos:", document_similarity(ngrams_a, ngrams_b))
    
    documents_ngrams = {
        'doc1.txt': ['este es un', 'es un ejemplo', 'un ejemplo de'],
        'doc2.txt': ['es un ejemplo', 'un ejemplo de', 'ejemplo de texto'],
        'doc3.txt': ['otro documento', 'documento diferente', 'diferente contenido']
    }
    
    print("Matriz de similitud:", calculate_similarity_matrix(documents_ngrams))