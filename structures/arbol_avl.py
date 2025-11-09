
class NodoAVL:
    """Nodo de Árbol AVL"""
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izquierdo: 'NodoAVL' = None
        self.derecho: 'NodoAVL' = None
        self.altura = 1

class ArbolAVL:
    """Árbol AVL (árbol binario de búsqueda auto-balanceado)"""
    def __init__(self):
        self.raiz: NodoAVL = None

    def _altura(self, nodo):
        """Retorna la altura del nodo"""
        return nodo.altura if nodo else 0

    def _actualizar_altura(self, nodo):
        """Actualiza la altura del nodo"""
        nodo.altura = 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

    def _factor_balance(self, nodo):
        """Calcula el factor de balance del nodo"""
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho)

    def _rotar_derecha(self, y):
        """Rotación simple a la derecha"""
        x = y.izquierdo
        T2 = x.derecho
        x.derecho = y
        y.izquierdo = T2
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotar_izquierda(self, x):
        """Rotación simple a la izquierda"""
        y = x.derecho
        T2 = y.izquierdo
        y.izquierdo = x
        x.derecho = T2
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    def insertar(self, clave, valor):
        """Inserta un par clave-valor en el árbol"""
        def _insertar(nodo, clave, valor):
            if not nodo:
                return NodoAVL(clave, valor)
            if clave < nodo.clave:
                nodo.izquierdo = _insertar(nodo.izquierdo, clave, valor)
            elif clave > nodo.clave:
                nodo.derecho = _insertar(nodo.derecho, clave, valor)
            else:
                nodo.valor = valor
                return nodo
            self._actualizar_altura(nodo)
            return self._rebalancear(nodo)
        self.raiz = _insertar(self.raiz, clave, valor)

    def _rebalancear(self, nodo):
        """Rebalancea el árbol si es necesario"""
        fb = self._factor_balance(nodo)
        if fb > 1:
            if self._factor_balance(nodo.izquierdo) < 0:
                nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)
        if fb < -1:
            if self._factor_balance(nodo.derecho) > 0:
                nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)
        return nodo

    def buscar(self, clave):
        """Busca un valor por su clave"""
        actual = self.raiz
        while actual:
            if clave == actual.clave:
                return actual.valor
            actual = actual.izquierdo if clave < actual.clave else actual.derecho
        return None

    def recorrido_inorden(self, visitar):
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
            while n.izquierdo:
                n = n.izquierdo
            return n

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
            self._actualizar_altura(nodo)
            return self._rebalancear(nodo)
        self.raiz = _eliminar(self.raiz, clave)
