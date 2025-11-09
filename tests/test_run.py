from services.library_service import LibraryService

def run_tests():
    service = LibraryService()
    u = service.agregar_usuario("u1", "Juan Perez", "juan@example.com")
    assert service.buscar_usuario("u1") is not None
    b = service.agregar_libro("L100", "Cien Años de Soledad", "G.G. Marquez", "Sudamericana", 1967, "Novela", 3)
    assert service.buscar_libro("L100") is not None
    p = service.crear_prestamo("u1", "L100")
    assert p.id_prestamo in service.prestamos
    assert service.buscar_libro("L100").copias_disponibles == 2
    service.devolver_prestamo(p.id_prestamo)
    assert service.buscar_libro("L100").copias_disponibles == 3
    resultados = service.buscar_por_prefijo_titulo("Cien")
    assert len(resultados) >= 1
    print("Todas las pruebas básicas pasaron.")

if __name__ == "__main__":
    run_tests()