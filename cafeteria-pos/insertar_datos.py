

print("Paso 1: iniciando script")

from supabase import create_client
from dotenv import load_dotenv
import os

print("Paso 2: librerías importadas")

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

print("Paso 3: URL =", url)
print("Paso 4: KEY primeros 10 =", key[:10] if key else "NO ENCONTRADA")

supabase = create_client(url, key)
print("Paso 5: cliente creado")

empleados = [
    {"nombre": "Ana Torres", "rol": "cajera"},
    {"nombre": "Luis Pérez", "rol": "barista"}
]
response = supabase.table("empleados").insert(empleados).execute()
print("Paso 6: empleados insertados:", response.data)

productos = [
    {"nombre": "Café americano", "categoria": "bebidas", "precio": 35.00, "stock_actual": 100, "stock_minimo": 10},
    {"nombre": "Café latte", "categoria": "bebidas", "precio": 45.00, "stock_actual": 80, "stock_minimo": 10},
    {"nombre": "Croissant", "categoria": "panadería", "precio": 30.00, "stock_actual": 50, "stock_minimo": 5},
    {"nombre": "Muffin de chocolate", "categoria": "panadería", "precio": 32.00, "stock_actual": 40, "stock_minimo": 5}
]
response = supabase.table("productos").insert(productos).execute()
print("Paso 7: productos insertados:", response.data)