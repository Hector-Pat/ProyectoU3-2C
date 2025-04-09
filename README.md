# Detector de Plagio para Trabajos Estudiantiles

## Descripción

Sistema de detección de plagio que identifica similitudes entre trabajos estudiantiles.

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
```bash
git clone https://github.com/tu-usuario/detector-plagio.git
cd detector-plagio
