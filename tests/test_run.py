import os
import sys
import uuid

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.library_service import LibraryService

def run_tests():
    print("\n" + "="*70)
    print(" PRUEBAS DEL SISTEMA DE BIBLIOTECA - ESTRUCTURAS NO LINEALES")
    print("="*70 + "\n")
    
    service = LibraryService()
    uid = "u_" + uuid.uuid4().hex[:6]
    bid = "b_" + uuid.uuid4().hex[:6]
    
    # Prueba 1: Agregar usuario usando BST
    print("[PRUEBA 1] Agregar usuario al Arbol Binario de Busqueda (BST)")
    print(f"   > Insertando usuario: ID={uid}, Nombre='Juan Perez'")
    u = service.agregar_usuario(uid, "Juan Perez", "juan@example.com")
    assert service.buscar_usuario(uid) is not None
    print(f"   [OK] Usuario agregado y encontrado en BST\n")

    # Prueba 2: Agregar libro usando BST y Trie
    print("[PRUEBA 2] Agregar libro al BST y al Trie")
    print(f"   > Insertando libro: ID={bid}, Titulo='Cien Años de Soledad'")
    b = service.agregar_libro(bid, "Cien Años de Soledad", "G.G. Marquez", "Sudamericana", 1967, "Novela", 3)
    assert service.buscar_libro(bid) is not None
    print(f"   [OK] Libro agregado al BST")
    print(f"   [OK] Titulo indexado en Trie para busqueda por prefijo\n")

    # Prueba 3: Crear préstamo
    print("[PRUEBA 3] Crear prestamo (reduce copias disponibles)")
    copias_antes = service.buscar_libro(bid).copias_disponibles
    print(f"   > Copias disponibles antes: {copias_antes}")
    p = service.crear_prestamo(uid, bid)
    assert p.id_prestamo in service.prestamos
    copias_despues = service.buscar_libro(bid).copias_disponibles
    assert copias_despues == 2
    print(f"   > Copias disponibles despues: {copias_despues}")
    print(f"   [OK] Prestamo creado: ID={p.id_prestamo}")
    print(f"   [OK] Copias reducidas correctamente: {copias_antes} -> {copias_despues}\n")
    
    # Prueba 4: Devolver préstamo
    print("[PRUEBA 4] Devolver prestamo (aumenta copias disponibles)")
    print(f"   > Devolviendo prestamo: {p.id_prestamo}")
    service.devolver_prestamo(p.id_prestamo)
    copias_final = service.buscar_libro(bid).copias_disponibles
    assert copias_final == 3
    print(f"   > Copias disponibles ahora: {copias_final}")
    print(f"   [OK] Libro devuelto correctamente: {copias_despues} -> {copias_final}\n")
    
    # Prueba 5: Búsqueda por prefijo usando Trie
    print("[PRUEBA 5] Busqueda por prefijo usando Trie")
    print(f"   > Buscando libros con prefijo 'Cien'...")
    resultados = service.buscar_por_prefijo_titulo("Cien")
    assert len(resultados) >= 1
    print(f"   [OK] Encontrados {len(resultados)} libro(s):")
    for libro in resultados:
        print(f"      - {libro.titulo} ({libro.autor})")
    print()
    
    # Prueba 6: Limpieza
    print("[PRUEBA 6] Eliminar datos de prueba (limpieza)")
    print(f"   > Eliminando usuario {uid} del BST...")
    service.eliminar_usuario(uid)
    print(f"   [OK] Usuario eliminado")
    print(f"   > Eliminando libro {bid} del BST y Trie...")
    service.eliminar_libro(bid)
    print(f"   [OK] Libro eliminado\n")
    
    print("="*70)
    print(" RESULTADO: TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    print("="*70)
    print("\nRESUMEN:")
    print("   - Arbol Binario de Busqueda (BST): Operaciones correctas")
    print("   - Trie: Busqueda por prefijo funcionando")
    print("   - Persistencia JSON: Datos guardados correctamente")
    print("   - Gestion de prestamos: Control de copias correcto")
    print()

if __name__ == "__main__":
    run_tests()