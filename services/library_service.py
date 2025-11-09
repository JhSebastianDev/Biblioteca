import uuid
from structures.arbol_binario import ArbolBinarioBusqueda
from structures.arbol_avl import ArbolAVL
from structures.trie import Trie
from models.libro import Book
from models.usuario import User
from models.prestamo import Loan
from repository.persistencia import (cargar_libros, cargar_usuarios, cargar_prestamos,
                                     guardar_libros, guardar_usuarios, guardar_prestamos)

class LibraryService:
    def __init__(self, usar_avl_para_libros=False):
        self.libros_tree = ArbolBinarioBusqueda()
        self.libros_avl = ArbolAVL() if usar_avl_para_libros else None
        self.titulos_trie = Trie()
        # Se usa BST también para usuarios (suficiente si no se esperan millones de nodos)
        self.usuarios_tree = ArbolBinarioBusqueda()
        self.prestamos = {}
        self._cargar_datos()

    def _cargar_datos(self):
        libros = cargar_libros()
        for libro in libros:
            self.libros_tree.insertar(libro.id_libro, libro)
            if self.libros_avl:
                self.libros_avl.insertar(libro.id_libro, libro)
            self.titulos_trie.insertar(libro.titulo, libro.id_libro)

        usuarios = cargar_usuarios()
        for usuario in usuarios:
            self.usuarios_tree.insertar(usuario.id_usuario, usuario)

        prestamos = cargar_prestamos()
        for prestamo in prestamos:
            self.prestamos[prestamo.id_prestamo] = prestamo

    def _persistir(self):
        libros_list = []
        self.libros_tree.recorrido_inorden(lambda k, v: libros_list.append(v))
        guardar_libros(libros_list)

        usuarios_list = []
        self.usuarios_tree.recorrido_inorden(lambda k, v: usuarios_list.append(v))
        guardar_usuarios(usuarios_list)

        guardar_prestamos(list(self.prestamos.values()))

    def agregar_libro(self, id_libro, titulo, autor, editorial, anio, categoria, copias):
        if self.libros_tree.buscar(id_libro):
            raise ValueError("Libro ya existe")
        libro = Book(id_libro, titulo, autor, editorial, anio, categoria, copias, copias)
        self.libros_tree.insertar(id_libro, libro)
        if self.libros_avl:
            self.libros_avl.insertar(id_libro, libro)
        self.titulos_trie.insertar(titulo, id_libro)
        self._persistir()
        return libro

    def buscar_libro(self, id_libro):
        return self.libros_tree.buscar(id_libro)

    def buscar_por_prefijo_titulo(self, prefijo):
        ids = self.titulos_trie.buscar_prefijo(prefijo)
        return [self.libros_tree.buscar(i) for i in ids]

    def eliminar_libro(self, id_libro):
        libro = self.libros_tree.buscar(id_libro)
        if not libro:
            return False
        self.libros_tree.eliminar(id_libro)
        if self.libros_avl:
            self.libros_avl.eliminar(id_libro)
        self._persistir()
        return True

    # --- Nuevas operaciones (refinamiento de funciones legacy) ---
    def actualizar_libro(self, id_libro, **kwargs):
        """Actualiza campos del libro. Si se modifica copias_totales ajusta copias_disponibles.
        Reglas:
          - Si nuevo total es mayor: aumenta disponibles por la diferencia.
          - Si nuevo total es menor: reduce disponibles sin bajar de 0 y no puede quedar mayor que nuevo total.
        """
        libro = self.buscar_libro(id_libro)
        if not libro:
            return False
        if 'copias_totales' in kwargs:
            nuevo_total = kwargs['copias_totales']
            if nuevo_total < 0:
                raise ValueError("copias_totales no puede ser negativo")
            diferencia = nuevo_total - libro.copias_totales
            if diferencia > 0:
                libro.copias_disponibles += diferencia
            else:  # reducción
                # Garantiza que disponibles no exceda el nuevo total
                libro.copias_disponibles = min(libro.copias_disponibles, nuevo_total)
            libro.copias_totales = nuevo_total
            del kwargs['copias_totales']
        # Actualiza otros campos si existen
        for campo, valor in kwargs.items():
            if hasattr(libro, campo):
                setattr(libro, campo, valor)
        # Reinsertar en AVL si se usa (ID no cambia, no necesario en BST)
        if self.libros_avl:
            # Simple: delete + insert para reflejar cambios si orden dependiera de otro campo (aquí por id no cambia)
            pass
        self._persistir()
        return True

    def listar_libros(self):
        libros = []
        self.libros_tree.recorrido_inorden(lambda k, v: libros.append(v))
        return libros

    def buscar_libros_por_titulo_autor(self, query: str):
        q = query.lower()
        resultados = []
        def _visit(k, libro):
            if q in libro.titulo.lower() or q in libro.autor.lower():
                resultados.append(libro)
        self.libros_tree.recorrido_inorden(_visit)
        return resultados

    def agregar_usuario(self, id_usuario, nombre, email):
        if self.usuarios_tree.buscar(id_usuario):
            raise ValueError("Usuario existe")
        usuario = User(id_usuario, nombre, email)
        self.usuarios_tree.insertar(id_usuario, usuario)
        self._persistir()
        return usuario

    def buscar_usuario(self, id_usuario):
        return self.usuarios_tree.buscar(id_usuario)

    def eliminar_usuario(self, id_usuario):
        if not self.usuarios_tree.buscar(id_usuario):
            return False
        self.usuarios_tree.eliminar(id_usuario)
        self._persistir()
        return True

    def actualizar_usuario(self, id_usuario, **kwargs):
        usuario = self.buscar_usuario(id_usuario)
        if not usuario:
            return False
        for campo, valor in kwargs.items():
            if hasattr(usuario, campo):
                setattr(usuario, campo, valor)
        self._persistir()
        return True

    def listar_usuarios(self):
        usuarios = []
        self.usuarios_tree.recorrido_inorden(lambda k, v: usuarios.append(v))
        return usuarios

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

    def libros_prestados_usuario(self, id_usuario):
        """Devuelve lista de libros actualmente prestados (activos) por el usuario."""
        prestamos = [p for p in self.prestamos.values() if p.id_usuario == id_usuario and p.estado == 'activo']
        return [self.buscar_libro(p.id_libro) for p in prestamos]

    def usuarios_con_libro(self, id_libro):
        """Usuarios que tienen actualmente prestado el libro indicado."""
        activos = [p for p in self.prestamos.values() if p.id_libro == id_libro and p.estado == 'activo']
        return [self.buscar_usuario(p.id_usuario) for p in activos]