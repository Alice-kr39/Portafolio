
#inventario dentro de routes 


from fastapi import APIRouter, HTTPException
from database import get_connection
from schemas import InventarioUpdate, InventarioResponse

router = APIRouter(prefix="/inventario", tags=["Inventario"])

@router.get("/")
def listar_inventario():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT i.id, p.nombre, p.categoria, 
               i.stock, i.stock_minimo
        FROM inventario i
        JOIN productos p ON i.id_producto = p.id
    """)
    inventario = cursor.fetchall()
    conn.close()
    return inventario

@router.get("/alertas")
def productos_bajo_minimo():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT i.id, p.nombre, i.stock, i.stock_minimo
        FROM inventario i
        JOIN productos p ON i.id_producto = p.id
        WHERE i.stock < i.stock_minimo
    """)
    alertas = cursor.fetchall()
    conn.close()
    return {"productos_en_riesgo": alertas}

@router.put("/{id}")
def actualizar_stock(id: int, datos: InventarioUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE inventario SET stock=%s, stock_minimo=%s WHERE id=%s",
        (datos.stock, datos.stock_minimo, id)
    )
    conn.commit()
    conn.close()
    return {"mensaje": "Stock actualizado"}