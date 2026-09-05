
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def registrar_venta(empleado_id, productos_vendidos):
    """
    productos_vendidos: lista de diccionarios
    ejemplo: [{"producto_id": 1, "cantidad": 2}, {"producto_id": 3, "cantidad": 1}]
    """
    total_venta = 0
    detalles = []

    # 1. Calcular subtotales y total
    for item in productos_vendidos:
        producto = supabase.table("productos").select("*").eq("id", item["producto_id"]).execute()
        producto_data = producto.data[0]

        precio = producto_data["precio"]
        subtotal = precio * item["cantidad"]
        total_venta += subtotal

        detalles.append({
            "producto_id": item["producto_id"],
            "cantidad": item["cantidad"],
            "precio_unitario": precio,
            "subtotal": subtotal
        })

    # 2. Crear la venta
    venta = supabase.table("ventas").insert({
        "empleado_id": empleado_id,
        "total": total_venta
    }).execute()
    venta_id = venta.data[0]["id"]
    print(f"Venta #{venta_id} creada. Total: ${total_venta}")

    # 3. Insertar detalle_venta y actualizar stock
    for detalle in detalles:
        detalle["venta_id"] = venta_id
        supabase.table("detalle_venta").insert(detalle).execute()

        # Descontar stock
        producto_actual = supabase.table("productos").select("stock_actual").eq("id", detalle["producto_id"]).execute()
        stock_nuevo = producto_actual.data[0]["stock_actual"] - detalle["cantidad"]
        supabase.table("productos").update({"stock_actual": stock_nuevo}).eq("id", detalle["producto_id"]).execute()

        # Registrar movimiento de inventario
        supabase.table("inventario_movimientos").insert({
            "producto_id": detalle["producto_id"],
            "tipo": "venta",
            "cantidad": detalle["cantidad"],
            "motivo": f"Venta #{venta_id}"
        }).execute()

    print("Venta registrada completamente. Stock actualizado.")

# Prueba: vender 2 cafés americanos y 1 croissant, con el empleado Ana Torres (id=1)
registrar_venta(empleado_id=1, productos_vendidos=[
    {"producto_id": 1, "cantidad": 2},
    {"producto_id": 3, "cantidad": 1}
])