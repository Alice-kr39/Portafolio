

# API Gestión de Inventario

API REST construida con FastAPI y MySQL para gestionar productos e inventario en tiempo real.

## Tecnologías
- Python
- FastAPI
- MySQL
- Uvicorn
- mysql-connector-python

## Instalación
```bash
pip install -r requirements.txt
```

## Uso
```bash
uvicorn main:app --reload
```

Abre en el navegador:
```
http://127.0.0.1:8000/docs
```

## Endpoints

### Productos
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /productos/ | Listar todos |
| GET | /productos/{id} | Obtener uno |
| POST | /productos/ | Crear nuevo |
| PUT | /productos/{id} | Actualizar |
| DELETE | /productos/{id} | Eliminar |

### Inventario
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /inventario/ | Ver stock |
| GET | /inventario/alertas | Productos bajo mínimo |
| PUT | /inventario/{id} | Actualizar stock |

## Autor
Alicia Carballo / https://github.com/Alice-kr39/Portafolio.git
