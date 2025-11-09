# Sistema de Gestión de Biblioteca (Refinamiento 2)

## 1. Resumen
Este prototipo implementa estructuras de datos lineales y no lineales para gestionar libros, usuarios y préstamos. Se emplean árboles (BST, AVL) y un Trie para mejorar búsquedas.

## 2. Objetivos
- Representar eficientemente entidades y sus relaciones.
- Facilitar inserción, búsqueda y eliminación.
- Optimizar búsquedas de libros y usuarios.
- Mantener persistencia utilizando archivos JSON.

## 3. Estructuras de Datos
- BinarySearchTree para libros por ID.
- AVLTree para usuarios (garantiza balance).
- Trie para búsquedas por prefijo de título.
- Diccionario (hash) para préstamos activos.

## 4. Justificación
La mezcla de un BST y AVL permite comparar rendimiento y complejidad. El Trie aporta eficiencia en búsquedas de texto. El hash simplifica acceso directo a préstamos.

## 5. Operaciones Clave
- Libros: agregar, buscar, eliminar, búsqueda por prefijo.
- Usuarios: agregar, buscar, eliminar.
- Préstamos: crear, devolver, listar activos, historial por usuario.

## 6. Persistencia
Datos en JSON (libros, usuarios, préstamos). Al modificar estructuras, se reextrae un listado in-order y se serializa.

## 7. Complejidad
| Estructura | Insert | Buscar | Eliminar |
|------------|--------|--------|----------|
| BST        | O(log n)* | O(log n)* | O(log n)* |
| AVL        | O(log n) | O(log n) | O(log n) |
| Trie       | O(L)     | O(P + K) | (No implementada eliminación por simplicidad) |

(*) Degrada a O(n) en peor caso si el BST se desbalancea.

## 8. Estrategia de Pruebas
- Pruebas funcionales básicas en `tests/test_run.py`.
- Se pueden extender a pruebas de rendimiento generando muchos libros/usuarios.

## 9. Decisiones de Diseño
- Simplicidad y claridad sobre máxima optimización.
- No se implementó eliminación del Trie por alcance.
- UUID parcial para id de préstamos.

## 10. Desafíos
- Balance entre facilidad de uso y desempeño.
- Serialización de estructuras no lineales: se convierte a listas planas para persistir.

## 11. Mejoras Futuras
- Heap para priorizar préstamos por vencimiento.
- Índice secundario por autor.
- Interfaz gráfica (Tkinter / Web).
- Eliminación y reconstrucción eficiente del Trie.

## 12. Ejecución
```bash
python cli/menu.py
```

## 13. Requisitos No Funcionales
- Portabilidad: Python 3.10+
- Mantenibilidad: Código modular.
- Rendimiento: Operaciones críticas en O(log n).
- Simplicidad de despliegue: Archivos locales JSON.

## 14. Licencia
Proyecto académico.
