# Sistema de Gestión de Biblioteca

Sistema completo de gestión de biblioteca implementado con estructuras de datos no lineales (árboles binarios de búsqueda, AVL y Trie) con persistencia en JSON.

---

## ¿Qué hace este sistema?

Gestiona libros, usuarios y préstamos de una biblioteca usando árboles binarios para búsquedas eficientes:
- **Registrar y buscar libros** por ID o por título
- **Gestionar usuarios** con historial de préstamos
- **Crear préstamos** y devoluciones de libros
- **Búsquedas rápidas** por prefijo de título
- **Persistencia automática** en archivos JSON

---

## 🚀 Cómo ejecutar

```bash

python cli/menu.py


python tests/test_run.py
```

---

##  Estructuras de Datos Usadas

### 1. **ArbolBinarioBusqueda (BST)** - `structures/arbol_binario.py`
Árbol binario de búsqueda para indexar libros y usuarios por ID.

**¿Por qué?** 
- Búsqueda, inserción y eliminación en O(log n) promedio
- Simple de implementar y suficiente para datasets moderados
- Se usa para libros y usuarios

**Métodos:**
- `insertar(clave, valor)` - Agrega un elemento
- `buscar(clave)` - Busca por ID
- `eliminar(clave)` - Elimina un elemento
- `recorrido_inorden(funcion)` - Recorre todos los elementos ordenados


---

### 2. **ArbolAVL** - `structures/arbol_avl.py`
Árbol binario auto-balanceado (opcional para libros).

**¿Por qué?**
- Garantiza O(log n) incluso en el peor caso
- Usa rotaciones para mantener el balance
- Opción disponible si se activa: `LibraryService(usar_avl_para_libros=True)`

**Métodos:** (iguales que BST)
- `insertar(clave, valor)`
- `buscar(clave)`
- `eliminar(clave)`
- `recorrido_inorden(funcion)`

---

### 3. **Trie** - `structures/trie.py`
Árbol de prefijos para buscar libros por título.

**¿Por qué?**
- Búsqueda de palabras que empiezan con cierto prefijo
- Ideal para autocompletado de títulos
- Mucho más rápido que buscar en lista

**Métodos:**
- `insert(titulo, id_libro)` - Indexa un título
- `search_prefix(prefijo)` - Devuelve todos los IDs que empiezan con el prefijo


---

### 4. **Diccionario (Hash)** - Python nativo
Para préstamos activos.

**¿Por qué?**
- Acceso directo por `id_prestamo`
- O(1) para buscar/insertar/eliminar

---

## 📦 Modelos de Datos

### Libro (`models/libro.py`)
```python
- id_libro: str           # Identificador único
- titulo: str             # Título del libro
- autor: str              # Autor
- editorial: str          # Editorial
- anio: int               # Año de publicación
- categoria: str          # Género/categoría
- copias_totales: int     # Total de copias
- copias_disponibles: int # Copias disponibles para préstamo
```

### Usuario (`models/usuario.py`)
```python
- id_usuario: str    # Identificador único
- nombre: str        # Nombre completo
- email: str         # Email
- activo: bool       # Estado del usuario
- historial: List    # Lista de IDs de préstamos
```

### Préstamo (`models/prestamo.py`)
```python
- id_prestamo: str        # ID único del préstamo
- id_usuario: str         # Usuario que prestó
- id_libro: str           # Libro prestado
- fecha_prestamo: str     # Fecha inicio
- fecha_limite: str       # Fecha límite devolución
- fecha_devolucion: str   # Fecha real de devolución
- estado: str             # "activo" o "devuelto"
```

---

##  Operaciones Disponibles

### **Libros:**
- Agregar libro
- Buscar por ID
- Buscar por prefijo de título (Trie)
- Buscar por título/autor (substring)
- Listar todos los libros
- Actualizar información
- Eliminar libro

### **Usuarios:**
- Agregar usuario
- Buscar por ID
- Listar todos los usuarios
- Actualizar información
- Eliminar usuario

### **Préstamos:**
- Crear préstamo (reduce copias disponibles)
- Devolver libro (aumenta copias disponibles)
- Listar préstamos activos
- Ver historial de usuario
- Ver usuarios que tienen un libro

---

## Persistencia - `repository/persistencia.py`

Los datos se guardan automáticamente en archivos JSON:
- `data/libros.json` - Libros registrados
- `data/usuarios.json` - Usuarios registrados
- `data/prestamos.json` - Historial de préstamos

**Cómo funciona:**
1. Al iniciar, carga los datos desde JSON a los árboles
2. Cada operación (agregar, actualizar, eliminar) persiste automáticamente
3. Se recorre el árbol con `recorrido_inorden()` y se serializa a JSON

---

## Análisis de Complejidad

| Operación | BST | AVL | Trie | Hash |
|-----------|-----|-----|------|------|
| Insertar | O(log n) / O(n) | O(log n) | O(L) | O(1) |
| Buscar | O(log n) / O(n) | O(log n) | O(P) | O(1) |
| Eliminar | O(log n) / O(n) | O(log n) | - | O(1) |
| Recorrer | O(n) | O(n) | - | O(n) |

**Leyenda:**
- n = número de elementos
- L = longitud del título
- P = longitud del prefijo
- O(n) peor caso en BST ocurre si se insertan elementos ordenados

---


## 🎓 Decisiones de Diseño

### ¿Por qué BST en lugar de listas?
- **Búsqueda:** O(log n) vs O(n) en lista
- **Inserción ordenada:** Mantiene orden sin ordenar manualmente
- **Eliminación:** Más eficiente que reorganizar lista

### ¿Por qué AVL opcional?
- BST es suficiente para datasets pequeños/medianos
- AVL garantiza balance pero añade complejidad (rotaciones)
- Se puede activar si se detecta degradación de rendimiento

### ¿Por qué Trie para títulos?
- Búsqueda por prefijo es O(P) vs O(n*m) en lista
- Ideal para autocompletado
- No se implementó eliminación (reconstrucción manual si es necesario)

### ¿Por qué diccionario para préstamos?
- Acceso directo por ID del préstamo
- No se necesita orden ni búsqueda por rango

---

##  Pruebas

El archivo `tests/test_run.py` valida:
-  Crear usuario y libro con IDs únicos
-  Buscar usuario y libro
-  Crear préstamo (reduce copias)
-  Devolver préstamo (aumenta copias)
-  Búsqueda por prefijo de título
-  Limpieza de datos de prueba

```bash
python tests/test_run.py

```

---

##  Requerimientos Cumplidos

### Funcionales:
 Gestión completa de libros (CRUD + búsquedas)  
 Gestión completa de usuarios (CRUD)  
 Gestión de préstamos y devoluciones  
 Persistencia en JSON  
 Búsquedas por prefijo con Trie  
 Menú CLI funcional  

### No Funcionales:
 Python 3.10+  
 Código modular (modelos, servicios, estructuras separadas)  
 Complejidad O(log n) en operaciones críticas  
 Sin dependencias externas (solo stdlib)  
 Nombres en español para mejor comprensión  

---


## Autor

JhSebastianDev
