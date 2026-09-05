

"""
- Pedir el empleado que está vendiendo
- Preguntar qué productos va agregando (uno por uno)
- Cuando termine, mostrar el resumen y confirmar
- Registrar todo (usando la misma función que ya construimos)"""






from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


def mostrar_productos():
    productos = supabase.table("productos").select("*").execute()
    print("\n--- PRODUCTOS DISPONIBLES ---")
    for p in productos.data:
        print(f"ID: {p['id']} | {p['nombre']} | ${p['precio']} | Stock: {p['stock_actual']}")
    print("------------------------------\n")


def registrar_venta(empleado_id, productos_vendidos):
    total_venta = 0
    detalles = []

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

    venta = supabase.table("ventas").insert({
        "empleado_id": empleado_id,
        "total": total_venta
    }).execute()
    venta_id = venta.data[0]["id"]

    for detalle in detalles:
        detalle["venta_id"] = venta_id
        supabase.table("detalle_venta").insert(detalle).execute()

        producto_actual = supabase.table("productos").select("stock_actual").eq("id", detalle["producto_id"]).execute()
        stock_nuevo = producto_actual.data[0]["stock_actual"] - detalle["cantidad"]
        supabase.table("productos").update({"stock_actual": stock_nuevo}).eq("id", detalle["producto_id"]).execute()

        supabase.table("inventario_movimientos").insert({
            "producto_id": detalle["producto_id"],
            "tipo": "venta",
            "cantidad": detalle["cantidad"],
            "motivo": f"Venta #{venta_id}"
        }).execute()

    return venta_id, total_venta


def punto_de_venta():
    print("=== PUNTO DE VENTA - CAFETERÍA ===\n")

    empleado_id = int(input("ID del empleado que atiende: "))
    mostrar_productos()

    carrito = []
    while True:
        producto_id = input("ID del producto a vender (o 'fin' para terminar): ")
        if producto_id.lower() == "fin":
            break

        cantidad = int(input("Cantidad: "))
        carrito.append({"producto_id": int(producto_id), "cantidad": cantidad})
        print(f"Agregado: producto {producto_id}, cantidad {cantidad}\n")

    if not carrito:
        print("No se agregó ningún producto. Venta cancelada.")
        return

    venta_id, total = registrar_venta(empleado_id, carrito)
    print(f"\n✅ Venta #{venta_id} registrada. Total: ${total}")


if __name__ == "__main__":
    punto_de_venta()