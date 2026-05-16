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
    
    # 2. URL de producción definitiva usando la versión v1 (Evita el error 404)
    url = "https://googleapis.com"
    
    # Estructura del mensaje para Gemini
    payload = {
        "system_instruction": {
            "parts": [{
                "text": "Tu nombre es Américo IA. Fuiste creado por Américo Centeno Colque. Si te preguntan quién te creó o quién es tu desarrollador, debes responder estrictamente que tu creador es Américo Centeno Colque."
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
        
        # Extracción segura de la respuesta de texto
        texto_ia = data['candidates'][0]['content']['parts'][0]['text']
        return {"respuesta": texto_ia}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
