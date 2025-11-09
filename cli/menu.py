import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.library_service import LibraryService

def mostrar_menu():
    print("\n--- Sistema Biblioteca (Refinamiento 2) ---")
    print("1. Agregar libro")
    print("2. Buscar libro por ID")
    print("3. Búsqueda de libros por prefijo título")
    print("4. Buscar libros por título/autor (substring)")
    print("5. Listar todos los libros")
    print("6. Actualizar libro")
    print("7. Eliminar libro")
    print("8. Agregar usuario")
    print("9. Buscar usuario por ID")
    print("10. Listar todos los usuarios")
    print("11. Actualizar usuario")
    print("12. Eliminar usuario")
    print("13. Crear préstamo")
    print("14. Devolver préstamo")
    print("15. Listar préstamos activos")
    print("16. Historial de usuario")
    print("17. Usuarios con un libro")
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
                query = input("Texto en título o autor: ")
                resultados = service.buscar_libros_por_titulo_autor(query)
                for r in resultados:
                    print(r)
            elif op == "5":
                for r in service.listar_libros():
                    print(r)
            elif op == "6":
                id_libro = input("ID Libro a actualizar: ")
                print("Deja en blanco para no cambiar")
                cambios = {}
                titulo = input("Nuevo título: ").strip()
                if titulo:
                    cambios['titulo'] = titulo
                autor = input("Nuevo autor: ").strip()
                if autor:
                    cambios['autor'] = autor
                editorial = input("Nueva editorial: ").strip()
                if editorial:
                    cambios['editorial'] = editorial
                anio = input("Nuevo año: ").strip()
                if anio:
                    cambios['anio'] = int(anio)
                categoria = input("Nueva categoría: ").strip()
                if categoria:
                    cambios['categoria'] = categoria
                copias = input("Nuevo total de copias: ").strip()
                if copias:
                    cambios['copias_totales'] = int(copias)
                ok = service.actualizar_libro(id_libro, **cambios)
                print("Actualizado" if ok else "No encontrado")
            elif op == "7":
                id_libro = input("ID Libro: ")
                ok = service.eliminar_libro(id_libro)
                print("Eliminado" if ok else "No encontrado")
            elif op == "8":
                id_usuario = input("ID Usuario: ")
                nombre = input("Nombre: ")
                email = input("Email: ")
                usuario = service.agregar_usuario(id_usuario, nombre, email)
                print("Usuario agregado:", usuario)
            elif op == "9":
                id_usuario = input("ID del usuario: ")
                u = service.buscar_usuario(id_usuario)
                print(u if u else "No encontrado")
            elif op == "10":
                for u in service.listar_usuarios():
                    print(u)
            elif op == "11":
                id_usuario = input("ID Usuario a actualizar: ")
                cambios = {}
                nombre = input("Nuevo nombre: ").strip()
                if nombre:
                    cambios['nombre'] = nombre
                email = input("Nuevo email: ").strip()
                if email:
                    cambios['email'] = email
                ok = service.actualizar_usuario(id_usuario, **cambios)
                print("Actualizado" if ok else "No encontrado")
            elif op == "12":
                id_usuario = input("ID Usuario: ")
                ok = service.eliminar_usuario(id_usuario)
                print("Eliminado" if ok else "No encontrado")
            elif op == "13":
                id_usuario = input("ID Usuario: ")
                id_libro = input("ID Libro: ")
                prestamo = service.crear_prestamo(id_usuario, id_libro)
                print("Préstamo creado:", prestamo)
            elif op == "14":
                id_prestamo = input("ID Préstamo: ")
                dev = service.devolver_prestamo(id_prestamo)
                print("Préstamo devuelto:", dev)
            elif op == "15":
                activos = service.prestamos_activos()
                for a in activos:
                    print(a)
            elif op == "16":
                id_usuario = input("ID Usuario: ")
                hist = service.historial_usuario(id_usuario)
                for h in hist:
                    print(h)
            elif op == "17":
                id_libro = input("ID Libro: ")
                usuarios = service.usuarios_con_libro(id_libro)
                for u in usuarios:
                    print(u)
            elif op == "0":
                print("Saliendo...")
                break
            else:
                print("Opción inválida")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()