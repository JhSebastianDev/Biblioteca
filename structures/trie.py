class TrieNode:
    def __init__(self):
        self.children = {}
        self.finishes = False
        self.ids_libros = set()

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, titulo: str, id_libro: str):
        node = self.root
        for ch in titulo.lower():
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.ids_libros.add(id_libro)
        node.finishes = True

    def search_prefix(self, prefijo: str):
        node = self.root
        for ch in prefijo.lower():
            if ch not in node.children:
                return set()
            node = node.children[ch]
        return node.ids_libros