import os
import requests
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI(title="API IA con API Key")

class DatosInput(BaseModel):
    prompt: str

@app.post("/chat")
def chatear(datos: DatosInput, x_api_key: str = Header(None)):
    
    # 1. Tu contraseña personal para asegurar la API
    if x_api_key != "AmericoSecreto764":
        raise HTTPException(status_code=401, detail="Acceso denegado: API Key Invalida.")
    
    # 2. Configuración de Hugging Face
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise HTTPException(status_code=500, detail="Falta configurar la variable HF_TOKEN en Render.")
    
    url = "https://huggingface.co"
    headers_hf = {"Authorization": f"Bearer {hf_token}"}
    
    instruccion_sistema = "Eres un asistente de IA útil y conciso."
    prompt_final = f"<bos><start_of_turn>user\nInstruccion: {instruccion_sistema}\nPregunta: {datos.prompt}\n<end_of_turn>\n<start_of_turn>model\n"
    
    payload = {
        "inputs": prompt_final,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.6,
            "return_full_text": False
        }
    }
    
    try:
        respuesta = requests.post(url, headers=headers_hf, json=payload)
        
        if respuesta.status_code != 200:
            raise HTTPException(
                status_code=respuesta.status_code, 
                detail=f"Error en Hugging Face: {respuesta.text}"
            )
            
        texto_generado = respuesta.json().get("generated_text", "")
        texto_limpio = texto_generado.replace("<end_of_turn>", "").strip()
        
        return {"respuesta_ia": texto_limpio}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
