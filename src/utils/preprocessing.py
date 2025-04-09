# Funciones para preprocesamiento de texto
"""
Módulo de preprocesamiento de texto
Limpia y tokeniza documentos para el detector de plagio
"""

import os
import re
import string

def clean_text(text):
    """
    Limpia el texto eliminando signos de puntuación y convirtiendo a minúsculas
    
    Args:
        text (str): Texto a limpiar
        
    Returns:
        str: Texto limpio
    """
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
    """
    Divide el texto en n-gramas
    
    Args:
        text (str): Texto limpio
        n (int): Tamaño del n-grama (2 para bi-gramas, 3 para tri-gramas, etc.)
        
    Returns:
        list: Lista de n-gramas
    """
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
    """
    Carga un documento desde un archivo
    
    Args:
        file_path (str): Ruta del archivo
        
    Returns:
        str: Contenido del archivo
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error al cargar el documento {file_path}: {e}")
        return ''

def load_documents_from_directory(dir_path):
    """
    Carga todos los documentos de un directorio
    
    Args:
        dir_path (str): Ruta del directorio
        
    Returns:
        dict: Diccionario con nombres de archivos como claves y contenido como valores
    """
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
    """
    Preprocesa un documento: lo limpia y genera n-gramas
    
    Args:
        text (str): Texto del documento
        n (int): Tamaño del n-grama
        
    Returns:
        list: Lista de n-gramas
    """
    cleaned_text = clean_text(text)
    return generate_ngrams(cleaned_text, n)

# Ejemplo de uso
if __name__ == "__main__":
    text = "Este es un ejemplo de texto. Contiene varias palabras y signos de puntuación."
    print("Texto original:", text)
    print("Texto limpio:", clean_text(text))
    print("Tri-gramas:", generate_ngrams(clean_text(text), 3))