"""
Script para ejecutar el detector de plagio con los 100 archivos generados
"""

import os
import sys
import time
from src.main import detect_plagiarism

def main():
    # Ruta a la carpeta con los 100 archivos - ACTUALIZA ESTA RUTA
    documents_dir = r"C:\Users\ferne\OneDrive\Documentos\100Archivos\archivos"
    
    # Verificar si la carpeta existe
    if not os.path.exists(documents_dir):
        print(f"Error: La carpeta {documents_dir} no existe.")
        print("Por favor, actualiza la ruta en el script o crea la carpeta con los archivos.")
        return
    
    # Contar archivos .txt en la carpeta
    txt_files = [f for f in os.listdir(documents_dir) if f.endswith('.txt')]
    file_count = len(txt_files)
    
    if file_count == 0:
        print(f"No se encontraron archivos .txt en {documents_dir}")
        return
    
    print(f"Se encontraron {file_count} archivos .txt en {documents_dir}")
    
    # Configuración del detector
    ngram_size = 3
    top_n = 20  # Mostrar los 20 pares más similares
    similarity_threshold = 0.3
    
    # Medir tiempo de ejecución
    start_time = time.time()
    
    # Ejecutar el detector de plagio
    detect_plagiarism(documents_dir, ngram_size, top_n, similarity_threshold)
    
    # Calcular tiempo de ejecución
    execution_time = time.time() - start_time
    print(f"\nTiempo de ejecución: {execution_time:.2f} segundos")

if __name__ == "__main__":
    main()