from typing import Optional, Callable

class NodoABB:
    """Nodo de Árbol Binario de Búsqueda"""
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izquierdo: Optional['NodoABB'] = None
        self.derecho: Optional['NodoABB'] = None

class ArbolBinarioBusqueda:
    """Árbol Binario de Búsqueda (Binary Search Tree)"""
    def __init__(self):
        self.raiz: Optional[NodoABB] = None

    def insertar(self, clave, valor):
        """Inserta un par clave-valor en el árbol"""
        def _insertar(nodo, clave, valor):
            if nodo is None:
                return NodoABB(clave, valor)
            if clave < nodo.clave:
                nodo.izquierdo = _insertar(nodo.izquierdo, clave, valor)
            elif clave > nodo.clave:
                nodo.derecho = _insertar(nodo.derecho, clave, valor)
            else:
                nodo.valor = valor
            return nodo
        self.raiz = _insertar(self.raiz, clave, valor)

    def buscar(self, clave):
        """Busca un valor por su clave"""
        nodo = self.raiz
        while nodo:
            if clave == nodo.clave:
                return nodo.valor
            nodo = nodo.izquierdo if clave < nodo.clave else nodo.derecho
        return None

    def recorrido_inorden(self, visitar: Callable):
        """Recorrido in-order del árbol"""
        def _inorden(nodo):
            if nodo:
                _inorden(nodo.izquierdo)
                visitar(nodo.clave, nodo.valor)
                _inorden(nodo.derecho)
        _inorden(self.raiz)

    def eliminar(self, clave):
        """Elimina un nodo por su clave"""
        def _nodo_minimo(n):
            actual = n
            while actual.izquierdo:
                actual = actual.izquierdo
            return actual

        def _eliminar(nodo, clave):
            if not nodo: return None
            if clave < nodo.clave:
                nodo.izquierdo = _eliminar(nodo.izquierdo, clave)
            elif clave > nodo.clave:
                nodo.derecho = _eliminar(nodo.derecho, clave)
            else:
                if not nodo.izquierdo: return nodo.derecho
                if not nodo.derecho: return nodo.izquierdo
                temp = _nodo_minimo(nodo.derecho)
                nodo.clave, nodo.valor = temp.clave, temp.valor
                nodo.derecho = _eliminar(nodo.derecho, temp.clave)
            return nodo
        self.raiz = _eliminar(self.raiz, clave)
