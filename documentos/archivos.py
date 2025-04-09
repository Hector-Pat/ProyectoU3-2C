import os
import random
import string

# Ruta personalizada en tu computadora
carpeta_destino = r"C:\Users\ferne\OneDrive\Documentos\100Archivos"

# Crear carpeta si no existe
os.makedirs(carpeta_destino, exist_ok=True)

# Palabras base para los textos
temas = [
    "La inteligencia artificial está transformando la educación moderna",
    "El cambio climático representa un gran desafío para la humanidad",
    "Los avances en medicina han mejorado la calidad de vida",
    "La tecnología influye en nuestras decisiones diarias",
    "La ética en la programación es fundamental para el futuro"
]

sinonimos = {
    "inteligencia": ["sabiduría", "cognición", "razón"],
    "climático": ["ambiental", "del clima", "ecológico"],
    "medicina": ["salud", "tratamiento", "cuidado"],
    "tecnología": ["innovación", "sistemas", "dispositivos"],
    "ética": ["moral", "valores", "principios"]
}

# Generar archivos
for i in range(100):
    contenido = []
    base = random.choice(temas)
    palabras = base.split()

    for _ in range(200):
        palabra = random.choice(palabras)
        if palabra in sinonimos and random.random() < 0.2:
            palabra = random.choice(sinonimos[palabra])
        contenido.append(palabra)
        if random.random() < 0.05:
            ruido = ''.join(random.choices(string.ascii_lowercase, k=5))
            contenido.append(ruido)

    texto_final = ' '.join(contenido)
    ruta_archivo = os.path.join(carpeta_destino, f"doc_{i+1}.txt")

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(texto_final)

print("✔ Archivos generados en:", carpeta_destino)
