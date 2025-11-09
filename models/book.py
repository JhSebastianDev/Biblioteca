from dataclasses import dataclass
from typing import Optional

@dataclass
class Book:
    id_libro: str
    titulo: str
    autor: str
    editorial: str
    anio: int
    categoria: str
    copias_totales: int
    copias_disponibles: int

    def to_dict(self):
        return {
            "id_libro": self.id_libro,
            "titulo": self.titulo,
            "autor": self.autor,
            "editorial": self.editorial,
            "anio": self.anio,
            "categoria": self.categoria,
            "copias_totales": self.copias_totales,
            "copias_disponibles": self.copias_disponibles,
        }

    @staticmethod
    def from_dict(data):
        return Book(**data)
