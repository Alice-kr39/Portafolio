

import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

st.set_page_config(page_title="Cafetería POS", page_icon="☕")
st.title("☕ Punto de Venta - Cafetería")

# Cargar empleados y productos
empleados = supabase.table("empleados").select("*").execute().data
productos = supabase.table("productos").select("*").execute().data

# Selección de empleado
nombres_empleados = {e["nombre"]: e["id"] for e in empleados}
empleado_nombre = st.selectbox("Empleado que atiende", list(nombres_empleados.keys()))
empleado_id = nombres_empleados[empleado_nombre]

st.divider()
st.subheader("Agregar productos a la venta")

# Carrito en memoria (se mantiene mientras usas la app)
if "carrito" not in st.session_state:
    st.session_state.carrito = []

nombres_productos = {p["nombre"]: p for p in productos}
producto_nombre = st.selectbox("Producto", list(nombres_productos.keys()))
cantidad = st.number_input("Cantidad", min_value=1, value=1, step=1)

if st.button("➕ Agregar al carrito"):
    producto = nombres_productos[producto_nombre]
    st.session_state.carrito.append({
        "producto_id": producto["id"],
        "nombre": producto["nombre"],
        "precio": producto["precio"],
        "cantidad": cantidad
    })
    st.success(f"Agregado: {cantidad} x {producto_nombre}")

# Mostrar carrito
st.divider()
st.subheader("🛒 Carrito actual")

if st.session_state.carrito:
    total = 0
    for item in st.session_state.carrito:
        subtotal = item["precio"] * item["cantidad"]
        total += subtotal
        st.write(f"{item['cantidad']} x {item['nombre']} — ${subtotal}")

    st.write(f"### Total: ${total}")

    if st.button("✅ Registrar venta"):
        venta = supabase.table("ventas").insert({
            "empleado_id": empleado_id,
            "total": total
        }).execute()
        venta_id = venta.data[0]["id"]

        for item in st.session_state.carrito:
            supabase.table("detalle_venta").insert({
                "venta_id": venta_id,
                "producto_id": item["producto_id"],
                "cantidad": item["cantidad"],
                "precio_unitario": item["precio"],
                "subtotal": item["precio"] * item["cantidad"]
            }).execute()

            producto_actual = supabase.table("productos").select("stock_actual").eq("id", item["producto_id"]).execute()
            stock_nuevo = producto_actual.data[0]["stock_actual"] - item["cantidad"]
            supabase.table("productos").update({"stock_actual": stock_nuevo}).eq("id", item["producto_id"]).execute()

            supabase.table("inventario_movimientos").insert({
                "producto_id": item["producto_id"],
                "tipo": "venta",
                "cantidad": item["cantidad"],
                "motivo": f"Venta #{venta_id}"
            }).execute()

        st.success(f"🎉 Venta #{venta_id} registrada exitosamente. Total: ${total}")
        st.session_state.carrito = []
else:
    st.info("El carrito está vacío. Agrega productos arriba.")