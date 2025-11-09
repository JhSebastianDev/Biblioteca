from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class Loan:
    id_prestamo: str
    id_usuario: str
    id_libro: str
    fecha_prestamo: str
    fecha_limite: str
    fecha_devolucion: Optional[str] = None
    estado: str = "activo"

    def to_dict(self):
        return {
            "id_prestamo": self.id_prestamo,
            "id_usuario": self.id_usuario,
            "id_libro": self.id_libro,
            "fecha_prestamo": self.fecha_prestamo,
            "fecha_limite": self.fecha_limite,
            "fecha_devolucion": self.fecha_devolucion,
            "estado": self.estado,
        }

    @staticmethod
    def crear(id_prestamo: str, id_usuario: str, id_libro: str, dias: int = 7):
        hoy = datetime.now()
        fecha_lim = hoy + timedelta(days=dias)
        return Loan(
            id_prestamo=id_prestamo,
            id_usuario=id_usuario,
            id_libro=id_libro,
            fecha_prestamo=hoy.isoformat(),
            fecha_limite=fecha_lim.isoformat()
        )

    @staticmethod
    def from_dict(data):
        return Loan(**data)