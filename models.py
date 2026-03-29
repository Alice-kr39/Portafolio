

#modelos api_inventario

from dataclasses import dataclass
from typing import Optional

@dataclass
class Producto:
    id: Optional[int]
    nombre: str
    categoria: str
    precio: float

@dataclass
class Inventario:
    id: Optional[int]
    id_producto: int
    stock: int
    stock_minimo: int