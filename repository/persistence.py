import json
from pathlib import Path
from models.book import Book
from models.user import User
from models.loan import Loan

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

PATH_LIBROS = DATA_DIR / "libros.json"
PATH_USUARIOS = DATA_DIR / "usuarios.json"
PATH_PRESTAMOS = DATA_DIR / "prestamos.json"

def guardar_libros(libros_list):
    with open(PATH_LIBROS, "w", encoding="utf-8") as f:
        json.dump([b.to_dict() for b in libros_list], f, ensure_ascii=False, indent=2)

def cargar_libros():
    if not PATH_LIBROS.exists():
        return []
    with open(PATH_LIBROS, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Book.from_dict(d) for d in data]

def guardar_usuarios(usuarios_list):
    with open(PATH_USUARIOS, "w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in usuarios_list], f, ensure_ascii=False, indent=2)

def cargar_usuarios():
    if not PATH_USUARIOS.exists():
        return []
    with open(PATH_USUARIOS, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [User.from_dict(d) for d in data]

def guardar_prestamos(prestamos_list):
    with open(PATH_PRESTAMOS, "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in prestamos_list], f, ensure_ascii=False, indent=2)

def cargar_prestamos():
    if not PATH_PRESTAMOS.exists():
        return []
    with open(PATH_PRESTAMOS, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Loan.from_dict(d) for d in data]