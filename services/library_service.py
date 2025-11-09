import uuid
from structures.bst import BinarySearchTree
from structures.avl import AVLTree
from structures.trie import Trie
from models.book import Book
from models.user import User
from models.loan import Loan
from repository.persistence import (cargar_libros, cargar_usuarios, cargar_prestamos,
                                    guardar_libros, guardar_usuarios, guardar_prestamos)

class LibraryService:
    def __init__(self, usar_avl_para_libros=False):
        self.libros_tree = BinarySearchTree()
        self.libros_avl = AVLTree() if usar_avl_para_libros else None
        self.titulos_trie = Trie()
        self.usuarios_tree = AVLTree()
        self.prestamos = {}
        self._cargar_datos()

    def _cargar_datos(self):
        libros = cargar_libros()
        for libro in libros:
            self.libros_tree.insert(libro.id_libro, libro)
            if self.libros_avl:
                self.libros_avl.insert(libro.id_libro, libro)
            self.titulos_trie.insert(libro.titulo, libro.id_libro)

        usuarios = cargar_usuarios()
        for usuario in usuarios:
            self.usuarios_tree.insert(usuario.id_usuario, usuario)

        prestamos = cargar_prestamos()
        for prestamo in prestamos:
            self.prestamos[prestamo.id_prestamo] = prestamo

    def _persistir(self):
        libros_list = []
        self.libros_tree.inorder(lambda k, v: libros_list.append(v))
        guardar_libros(libros_list)

        usuarios_list = []
        self.usuarios_tree.inorder(lambda k, v: usuarios_list.append(v))
        guardar_usuarios(usuarios_list)

        guardar_prestamos(list(self.prestamos.values()))

    def agregar_libro(self, id_libro, titulo, autor, editorial, anio, categoria, copias):
        if self.libros_tree.search(id_libro):
            raise ValueError("Libro ya existe")
        libro = Book(id_libro, titulo, autor, editorial, anio, categoria, copias, copias)
        self.libros_tree.insert(id_libro, libro)
        if self.libros_avl:
            self.libros_avl.insert(id_libro, libro)
        self.titulos_trie.insert(titulo, id_libro)
        self._persistir()
        return libro

    def buscar_libro(self, id_libro):
        return self.libros_tree.search(id_libro)

    def buscar_por_prefijo_titulo(self, prefijo):
        ids = self.titulos_trie.search_prefix(prefijo)
        return [self.libros_tree.search(i) for i in ids]

    def eliminar_libro(self, id_libro):
        libro = self.libros_tree.search(id_libro)
        if not libro:
            return False
        self.libros_tree.delete(id_libro)
        if self.libros_avl:
            self.libros_avl.delete(id_libro)
        self._persistir()
        return True

    def agregar_usuario(self, id_usuario, nombre, email):
        if self.usuarios_tree.search(id_usuario):
            raise ValueError("Usuario existe")
        usuario = User(id_usuario, nombre, email)
        self.usuarios_tree.insert(id_usuario, usuario)
        self._persistir()
        return usuario

    def buscar_usuario(self, id_usuario):
        return self.usuarios_tree.search(id_usuario)

    def eliminar_usuario(self, id_usuario):
        if not self.usuarios_tree.search(id_usuario):
            return False
        self.usuarios_tree.delete(id_usuario)
        self._persistir()
        return True

    def crear_prestamo(self, id_usuario, id_libro, dias=7):
        usuario = self.buscar_usuario(id_usuario)
        libro = self.buscar_libro(id_libro)
        if not usuario or not libro:
            raise ValueError("Usuario o Libro no existe")
        if libro.copias_disponibles <= 0:
            raise ValueError("No hay copias disponibles")
        id_prestamo = str(uuid.uuid4())[:8]
        prestamo = Loan.crear(id_prestamo, id_usuario, id_libro, dias)
        libro.copias_disponibles -= 1
        usuario.historial.append(id_prestamo)
        self.prestamos[id_prestamo] = prestamo
        self._persistir()
        return prestamo

    def devolver_prestamo(self, id_prestamo):
        prestamo = self.prestamos.get(id_prestamo)
        if not prestamo or prestamo.estado != "activo":
            raise ValueError("Préstamo inválido")
        libro = self.buscar_libro(prestamo.id_libro)
        libro.copias_disponibles += 1
        from datetime import datetime
        prestamo.fecha_devolucion = datetime.now().isoformat()
        prestamo.estado = "devuelto"
        self._persistir()
        return prestamo

    def prestamos_activos(self):
        return [p for p in self.prestamos.values() if p.estado == "activo"]

    def historial_usuario(self, id_usuario):
        usuario = self.buscar_usuario(id_usuario)
        if not usuario:
            return []
        return [self.prestamos[pid] for pid in usuario.historial if pid in self.prestamos]