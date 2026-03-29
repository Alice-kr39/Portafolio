

from fastapi import FastAPI
from routes import productos, inventario

app = FastAPI(
    title="API Gestión de Inventario",
    description="API REST para gestionar productos e inventario",
    version="1.0.0"
)

app.include_router(productos.router)
app.include_router(inventario.router)

@app.get("/")
def inicio():
    return {
        "mensaje": "API de Inventario funcionando",
        "version": "1.0.0",
        "docs": "/docs"
    }