import json
from pathlib import Path
from models.libro import Book
from models.usuario import User
from models.prestamo import Loan

DIRECTORIO_DATOS = Path("data")
DIRECTORIO_DATOS.mkdir(exist_ok=True)

RUTA_LIBROS = DIRECTORIO_DATOS / "libros.json"
RUTA_USUARIOS = DIRECTORIO_DATOS / "usuarios.json"
RUTA_PRESTAMOS = DIRECTORIO_DATOS / "prestamos.json"

def guardar_libros(lista_libros):
    """Guarda la lista de libros en formato JSON"""
    with open(RUTA_LIBROS, "w", encoding="utf-8") as f:
        json.dump([libro.to_dict() for libro in lista_libros], f, ensure_ascii=False, indent=2)

def cargar_libros():
    """Carga la lista de libros desde JSON"""
    if not RUTA_LIBROS.exists():
        return []
    with open(RUTA_LIBROS, "r", encoding="utf-8") as f:
        datos = json.load(f)
        return [Book.from_dict(d) for d in datos]

def guardar_usuarios(lista_usuarios):
    """Guarda la lista de usuarios en formato JSON"""
    with open(RUTA_USUARIOS, "w", encoding="utf-8") as f:
        json.dump([usuario.to_dict() for usuario in lista_usuarios], f, ensure_ascii=False, indent=2)

def cargar_usuarios():
    """Carga la lista de usuarios desde JSON"""
    if not RUTA_USUARIOS.exists():
        return []
    with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
        datos = json.load(f)
        return [User.from_dict(d) for d in datos]

def guardar_prestamos(lista_prestamos):
    """Guarda la lista de préstamos en formato JSON"""
    with open(RUTA_PRESTAMOS, "w", encoding="utf-8") as f:
        json.dump([prestamo.to_dict() for prestamo in lista_prestamos], f, ensure_ascii=False, indent=2)

def cargar_prestamos():
    """Carga la lista de préstamos desde JSON"""
    if not RUTA_PRESTAMOS.exists():
        return []
    with open(RUTA_PRESTAMOS, "r", encoding="utf-8") as f:
        datos = json.load(f)
        return [Loan.from_dict(d) for d in datos]
