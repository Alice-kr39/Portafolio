

#schemas api_inventario

from pydantic import BaseModel
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str
    categoria: str
    precio: float

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    categoria: str
    precio: float

class InventarioUpdate(BaseModel):
    stock: int
    stock_minimo: int

class InventarioResponse(BaseModel):
    id: int
    id_producto: int
    stock: int
    stock_minimo: int

    