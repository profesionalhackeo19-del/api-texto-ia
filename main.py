import os
import requests
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI(title="API IA de Américo")

class DatosInput(BaseModel):
    prompt: str

@app.post("/chat")
def chatear(datos: DatosInput, x_api_key: str = Header(None)):
    # 1. Tu contraseña personal de seguridad para proteger tu API
    if x_api_key != "AmericoSecreto764":
        raise HTTPException(status_code=401, detail="Acceso denegado: API Key Invalida.")
    
    # 2. Tu API Key de Gemini colocada exactamente donde corresponde
    GEMINI_API_KEY = "AIzaSyBlvVq5CxbXQejM1HSvOI4zZz6BPnrz1_0" 
    
    # URL oficial de la API de Gemini (Corregida con las barras y parámetros exactos)
    url = f"https://googleapis.com{GEMINI_API_KEY}"
    
    # Estructura JSON válida con las instrucciones de identidad para Google
    payload = {
        "system_instruction": {
            "parts": [{
                "text": "Tu nombre es Américo IA. Fuiste creado por Américo Centeno Colque. Si te preguntan quién te creó, quién es tu desarrollador o preguntas similares, debes responder estrictamente que tu creador es Américo Centeno Colque."
            }]
        },
        "contents": [{
            "parts": [{"text": datos.prompt}]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error de Gemini: {response.text}")
            
        data = response.json()
        
        # Extraer de forma precisa el texto devuelto por Google
        texto_ia = data['candidates'][0]['content']['parts'][0]['text']
        return {"respuesta": texto_ia}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
