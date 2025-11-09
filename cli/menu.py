from services.library_service import LibraryService

def mostrar_menu():
    print("\n--- Sistema Biblioteca (Refinamiento 2) ---")
    print("1. Agregar libro")
    print("2. Buscar libro por ID")
    print("3. Búsqueda de libros por prefijo título")
    print("4. Agregar usuario")
    print("5. Crear préstamo")
    print("6. Devolver préstamo")
    print("7. Listar préstamos activos")
    print("8. Historial de usuario")
    print("9. Eliminar libro")
    print("10. Eliminar usuario")
    print("0. Salir")

def main():
    service = LibraryService()
    while True:
        mostrar_menu()
        op = input("Opción: ").strip()
        try:
            if op == "1":
                id_libro = input("ID Libro: ")
                titulo = input("Título: ")
                autor = input("Autor: ")
                editorial = input("Editorial: ")
                anio = int(input("Año: "))
                categoria = input("Categoría: ")
                copias = int(input("Copias: "))
                libro = service.agregar_libro(id_libro, titulo, autor, editorial, anio, categoria, copias)
                print("Libro agregado:", libro)
            elif op == "2":
                id_libro = input("ID: ")
                libro = service.buscar_libro(id_libro)
                print(libro if libro else "No encontrado")
            elif op == "3":
                prefijo = input("Prefijo título: ")
                resultados = service.buscar_por_prefijo_titulo(prefijo)
                for r in resultados:
                    print(r)
            elif op == "4":
                id_usuario = input("ID Usuario: ")
                nombre = input("Nombre: ")
                email = input("Email: ")
                usuario = service.agregar_usuario(id_usuario, nombre, email)
                print("Usuario agregado:", usuario)
            elif op == "5":
                id_usuario = input("ID Usuario: ")
                id_libro = input("ID Libro: ")
                prestamo = service.crear_prestamo(id_usuario, id_libro)
                print("Préstamo creado:", prestamo)
            elif op == "6":
                id_prestamo = input("ID Préstamo: ")
                dev = service.devolver_prestamo(id_prestamo)
                print("Préstamo devuelto:", dev)
            elif op == "7":
                activos = service.prestamos_activos()
                for a in activos:
                    print(a)
            elif op == "8":
                id_usuario = input("ID Usuario: ")
                hist = service.historial_usuario(id_usuario)
                for h in hist:
                    print(h)
            elif op == "9":
                id_libro = input("ID Libro: ")
                ok = service.eliminar_libro(id_libro)
                print("Eliminado" if ok else "No encontrado")
            elif op == "10":
                id_usuario = input("ID Usuario: ")
                ok = service.eliminar_usuario(id_usuario)
                print("Eliminado" if ok else "No encontrado")
            elif op == "0":
                print("Saliendo...")
                break
            else:
                print("Opción inválida")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()