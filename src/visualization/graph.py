# Visualización de resultados
"""
Módulo para visualizar los resultados del detector de plagio
"""

def generate_ascii_graph(similarity_pairs, threshold=0.3):
    """
    Genera una representación en texto ASCII de un grafo de similitud
    
    Args:
        similarity_pairs (list): Pares de documentos con su similitud
        threshold (float): Umbral de similitud para mostrar conexiones
        
    Returns:
        str: Representación ASCII del grafo
    """
    # Filtrar pares por umbral de similitud
    filtered_pairs = [pair for pair in similarity_pairs if pair['similarity'] >= threshold]
    
    # Obtener todos los documentos únicos
    documents = set()
    for pair in filtered_pairs:
        documents.add(pair['doc_a'])
        documents.add(pair['doc_b'])
    
    doc_array = list(documents)
    
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
    """
    Genera una representación visual de la fuerza de conexión
    
    Args:
        similarity (float): Valor de similitud
        
    Returns:
        str: Representación visual
    """
    if similarity >= 0.8:
        return "====>"
    if similarity >= 0.6:
        return "===>"
    if similarity >= 0.4:
        return "==>"
    return "=>"

def generate_similarity_table(similarity_pairs):
    """
    Genera una tabla de similitud en formato de texto
    
    Args:
        similarity_pairs (list): Pares de documentos con su similitud
        
    Returns:
        str: Tabla de similitud
    """
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

# Ejemplo de uso
if __name__ == "__main__":
    similarity_pairs = [
        {'doc_a': 'doc1.txt', 'doc_b': 'doc2.txt', 'similarity': 0.85},
        {'doc_a': 'doc1.txt', 'doc_b': 'doc3.txt', 'similarity': 0.35},
        {'doc_a': 'doc2.txt', 'doc_b': 'doc3.txt', 'similarity': 0.55},
        {'doc_a': 'doc3.txt', 'doc_b': 'doc4.txt', 'similarity': 0.55},
        {'doc_a': 'doc3.txt', 'doc_b': 'doc4.txt', 'similarity': 0.25},
        {'doc_a': 'doc4.txt', 'doc_b': 'doc5.txt', 'similarity': 0.15}
    ]
    
    print(generate_ascii_graph(similarity_pairs, 0.3))
    print(generate_similarity_table(similarity_pairs))