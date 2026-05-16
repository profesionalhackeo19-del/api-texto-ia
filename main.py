import os
import requests
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI(title="API IA de Américo")

class DatosInput(BaseModel):
    prompt: str

@app.post("/chat")
def chatear(datos: DatosInput, x_api_key: str = Header(None)):
    
    # 1. Tu contraseña personal de seguridad
    if x_api_key != "AmericoSecreto764":
        raise HTTPException(status_code=401, detail="Acceso denegado: API Key Invalida.")
    
    # 2. Obtener la clave gratuita de Gemini desde Render
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise HTTPException(status_code=500, detail="Falta configurar la variable GEMINI_API_KEY en Render.")
    
    # URL oficial de la API de Google Gemini (Modelo rápido y gratuito)
    url = f"https://googleapis.com{gemini_key}"
    
    # Instrucción para que recuerde tu nombre
    contexto = (
        "Tu creador es Américo Centeno Colque. Si te preguntan quién te creó, "
        "quién es tu creador o desarrollador, responde con orgullo que fuiste creado por Américo Centeno Colque. "
        "Responde a la siguiente petición del usuario basándote en esto: "
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{contexto}{datos.prompt}"}]
        }]
    }
    
    try:
        respuesta = requests.post(url, json=payload)
        
        if respuesta.status_code != 200:
            raise HTTPException(status_code=respuesta.status_code, detail=f"Error en Google Gemini: {respuesta.text}")
            
        data = respuesta.json()
        # Extraer la respuesta de texto limpia de Google
        texto_ia = data['candidates'][0]['content']['parts'][0]['text']
        return {"respuesta_ia": texto_ia.strip()}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
