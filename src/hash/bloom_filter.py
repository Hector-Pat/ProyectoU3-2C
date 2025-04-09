# Implementación de filtro de Bloom
"""
Implementación de un Filtro de Bloom para optimizar la memoria
Un filtro de Bloom es una estructura de datos probabilística que permite
verificar si un elemento está en un conjunto de manera eficiente
"""

class BloomFilter:
    """
    Clase BloomFilter - Implementación de un filtro de Bloom
    """
    
    def __init__(self, size=10000, hash_count=3):
        """
        Constructor del filtro de Bloom
        
        Args:
            size (int): Tamaño del filtro (número de bits)
            hash_count (int): Número de funciones hash a utilizar
        """
        self.size = size
        self.hash_count = hash_count
        # Crear un array de bits (representado como un array de booleanos)
        self.bit_array = [False] * size
    
    def add(self, item):
        """
        Agrega un elemento al filtro
        
        Args:
            item (str): Elemento a agregar
        """
        # Aplicar cada función hash y marcar los bits correspondientes
        for index in self._get_hash_values(item):
            self.bit_array[index] = True
    
    def contains(self, item):
        """
        Verifica si un elemento podría estar en el filtro
        
        Args:
            item (str): Elemento a verificar
            
        Returns:
            bool: True si el elemento podría estar, False si definitivamente no está
        """
        # Verificar si todos los bits correspondientes están marcados
        return all(self.bit_array[index] for index in self._get_hash_values(item))
    
    def _get_hash_values(self, item):
        """
        Obtiene los índices hash para un elemento
        
        Args:
            item (str): Elemento a hashear
            
        Returns:
            list: Lista de índices hash
        """
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
        """
        Función hash 1
        
        Args:
            string (str): Cadena a hashear
            
        Returns:
            int: Valor hash
        """
        hash_value = 0
        for char in string:
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value
    
    def _hash2(self, string):
        """
        Función hash 2
        
        Args:
            string (str): Cadena a hashear
            
        Returns:
            int: Valor hash
        """
        hash_value = 0
        for char in string:
            hash_value = (hash_value * 37 + ord(char)) % self.size
        return hash_value
    
    def _hash3(self, string):
        """
        Función hash 3
        
        Args:
            string (str): Cadena a hashear
            
        Returns:
            int: Valor hash
        """
        hash_value = 0
        for char in string:
            hash_value = (hash_value * 17 + ord(char)) % self.size
        return hash_value
    
    def clear(self):
        """
        Limpia el filtro
        """
        self.bit_array = [False] * self.size
    
    def get_false_positive_rate(self, item_count):
        """
        Calcula la tasa de falsos positivos estimada
        
        Args:
            item_count (int): Número de elementos insertados
            
        Returns:
            float: Tasa de falsos positivos
        """
        # Fórmula: (1 - e^(-k*n/m))^k
        # k: número de funciones hash
        # n: número de elementos insertados
        # m: tamaño del filtro
        import math
        k = self.hash_count
        m = self.size
        n = item_count
        
        return (1 - math.exp(-k * n / m)) ** k

# Ejemplo de uso
if __name__ == "__main__":
    bloom_filter = BloomFilter(1000, 3)
    
    # Agregar algunos elementos
    bloom_filter.add("este es un")
    bloom_filter.add("es un ejemplo")
    bloom_filter.add("un ejemplo de")
    
    # Verificar si los elementos están en el filtro
    print("'este es un' está en el filtro:", bloom_filter.contains("este es un"))
    print("'no existe' está en el filtro:", bloom_filter.contains("no existe"))
    
    # Calcular la tasa de falsos positivos
    print("Tasa de falsos positivos estimada:", bloom_filter.get_false_positive_rate(3))