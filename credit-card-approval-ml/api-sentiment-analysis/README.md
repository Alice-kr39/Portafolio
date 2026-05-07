
# Sentiment Analysis API

# Descripción
API REST construida con FastAPI que analiza el sentimiento 
de textos en inglés, clasificándolos como positivo, 
negativo o neutral en tiempo real.

#Tecnologías
- Python
- FastAPI
- TextBlob
- Uvicorn

## Instalación
pip install fastapi uvicorn textblob

#Uso
Inicia el servidor:
uvicorn main:app --reload

Visita la documentación interactiva:
http://127.0.0.1:8000/docs

#Endpoint
POST /analizar
- Parámetro: texto (string)
- Respuesta: sentimiento + polaridad

## Ejemplo de respuesta
{
  "texto": "This product is amazing",
  "sentimiento": "Positivo 😊",
  "polaridad": 0.6
}

#Limitaciones conocidas
- TextBlob analiza únicamente textos en inglés
- No detecta sarcasmo ni modismos culturales
- Para análisis en español o mayor precisión
  se recomienda integrar un modelo de IA generativa

#Autor
ALicia Carballo Uicab
