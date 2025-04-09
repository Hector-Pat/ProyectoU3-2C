"""
Implementación de una tabla hash para almacenar n-gramas
"""

def custom_hash(string, table_size):
    """
    Función hash personalizada para cadenas de texto
    
    Args:
        string (str): Cadena a hashear
        table_size (int): Tamaño de la tabla hash
        
    Returns:
        int: Valor hash
    """
    hash_value = 0
    PRIME = 31
    
    for char in string:
        # Multiplicamos el hash actual por un número primo y sumamos el código del carácter
        hash_value = (hash_value * PRIME + ord(char)) % table_size
    
    return hash_value

class HashTable:
    """
    Clase HashTable - Implementación de una tabla hash con manejo de colisiones por encadenamiento
    """
    
    def __init__(self, size=1024):
        """
        Constructor de la tabla hash
        
        Args:
            size (int): Tamaño inicial de la tabla
        """
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0
    
    def insert(self, key, value):
        """
        Inserta un elemento en la tabla hash
        
        Args:
            key (str): Clave (n-grama)
            value (any): Valor asociado (generalmente el documento)
        """
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
        """
        Busca un elemento en la tabla hash
        
        Args:
            key (str): Clave a buscar
            
        Returns:
            any: Valor asociado o None si no se encuentra
        """
        index = custom_hash(key, self.size)
        
        bucket = self.table[index]
        for item in bucket:
            if item[0] == key:
                return item[1]
        
        return None
    
    def _resize(self, new_size):
        """
        Redimensiona la tabla hash
        
        Args:
            new_size (int): Nuevo tamaño de la tabla
        """
        old_table = self.table
        self.size = new_size
        self.table = [[] for _ in range(new_size)]
        self.count = 0
        
        # Reinserta todos los elementos
        for bucket in old_table:
            for key, values in bucket:
                for value in values:
                    self.insert(key, value)
    
    def keys(self):
        """
        Obtiene todas las claves de la tabla hash
        
        Returns:
            list: Lista de claves
        """
        all_keys = []
        
        for bucket in self.table:
            for key, _ in bucket:
                all_keys.append(key)
        
        return all_keys
    
    def values(self):
        """
        Obtiene todos los valores de la tabla hash
        
        Returns:
            list: Lista de valores
        """
        all_values = []
        
        for bucket in self.table:
            for _, values in bucket:
                all_values.extend(values)
        
        return list(set(all_values))  # Eliminar duplicados
    
    def entries(self):
        """
        Obtiene todos los pares clave-valor de la tabla hash
        
        Returns:
            list: Lista de tuplas (key, value)
        """
        all_entries = []
        
        for bucket in self.table:
            for key, values in bucket:
                all_entries.append((key, values))
        
        return all_entries

# Ejemplo de uso
if __name__ == "__main__":
    hash_table = HashTable(10)
    
    hash_table.insert("este es un", "doc1")
    hash_table.insert("es un ejemplo", "doc1")
    hash_table.insert("un ejemplo de", "doc1")
    hash_table.insert("este es un", "doc2")
    
    print("Búsqueda 'este es un':", hash_table.search("este es un"))
    print("Búsqueda 'no existe':", hash_table.search("no existe"))
    print("Claves:", hash_table.keys())
    print("Valores:", hash_table.values())