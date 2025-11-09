from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    id_usuario: str
    nombre: str
    email: str
    activo: bool = True
    historial: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "email": self.email,
            "activo": self.activo,
            "historial": self.historial,
        }

    @staticmethod
    def from_dict(data):
        return User(**data)
