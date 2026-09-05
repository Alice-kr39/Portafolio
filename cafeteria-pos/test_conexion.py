
print("Paso 1: iniciando script")

from supabase import create_client
from dotenv import load_dotenv
import os

print("Paso 2: librerías importadas correctamente")

load_dotenv()
print("Paso 3: .env cargado")

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

print("Paso 4: URL leída:", url)
print("Paso 5: KEY leída (primeros 10 caracteres):", key[:10] if key else "NO SE ENCONTRÓ")

supabase = create_client(url, key)
print("Paso 6: cliente creado")

response = supabase.table("empleados").select("*").execute()
print("Paso 7: consulta ejecutada")

print("Conexión exitosa. Datos de empleados:")
print(response.data)