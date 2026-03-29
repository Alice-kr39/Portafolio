

#routes  api_inventario



from fastapi import APIRouter, HTTPException
from database import get_connection
from schemas import ProductoCreate, ProductoResponse

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/")
def listar_productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

@router.get("/{id}")
def obtener_producto(id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    conn.close()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/")
def crear_producto(producto: ProductoCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, categoria, precio) VALUES (%s, %s, %s)",
        (producto.nombre, producto.categoria, producto.precio)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return {"mensaje": "Producto creado", "id": nuevo_id}

@router.put("/{id}")
def actualizar_producto(id: int, producto: ProductoCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=%s, categoria=%s, precio=%s WHERE id=%s",
        (producto.nombre, producto.categoria, producto.precio, id)
    )
    conn.commit()
    conn.close()
    return {"mensaje": "Producto actualizado"}

@router.delete("/{id}")
def eliminar_producto(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return {"mensaje": "Producto eliminado"}
