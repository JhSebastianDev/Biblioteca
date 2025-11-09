class NodoTrie:
    """Nodo del árbol Trie para búsqueda por prefijos"""
    def __init__(self):
        self.hijos = {}
        self.es_final = False
        self.ids_libros = set()

class Trie:
    """Árbol Trie para búsqueda eficiente de títulos por prefijo"""
    def __init__(self):
        self.raiz = NodoTrie()

    def insertar(self, titulo: str, id_libro: str):
        """Inserta un título y su ID en el Trie"""
        nodo = self.raiz
        for caracter in titulo.lower():
            if caracter not in nodo.hijos:
                nodo.hijos[caracter] = NodoTrie()
            nodo = nodo.hijos[caracter]
            nodo.ids_libros.add(id_libro)
        nodo.es_final = True

    def buscar_prefijo(self, prefijo: str):
        """Busca todos los libros que empiezan con el prefijo dado"""
        nodo = self.raiz
        for caracter in prefijo.lower():
            if caracter not in nodo.hijos:
                return set()
            nodo = nodo.hijos[caracter]
        return nodo.ids_libros