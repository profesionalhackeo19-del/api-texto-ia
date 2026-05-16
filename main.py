import os
import requests
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN

app = FastAPI(title="API IA con API Key")

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

MI_API_KEY_SECRETA = os.getenv("MI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
headers_hf = {"Authorization": f"Bearer {HF_TOKEN}"}

async def verificar_api_key(api_key: str = Depends(api_key_header)):
    if api_key == MI_API_KEY_SECRETA and MI_API_KEY_SECRETA is not None:
        return api_key
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, 
        detail="Acceso denegado: API Key invalida."
    )

class EntradaTexto(BaseModel):
    prompt: str

@app.get("/")
def estado():
    return {"mensaje": "API protegida activa"}

@app.post("/chat")
def chatear(datos: EntradaTexto, api_key: str = Depends(verificar_api_key)):
    if not HF_TOKEN: 
        raise HTTPException(status_code=500, detail="Falta configurar HF_TOKEN")
    
    url = "https://huggingface.co"
    nombre_creador = "Americo centeno colque"
    
    instruccion_sistema = (
        f"Eres una inteligencia artificial. Tu creador es {nombre_creador}. "
        f"Si te preguntan quien te creo, debes responder obligatoriamente de forma clara "
        f"que fuiste creado por {nombre_creador}. Responde en espanol de forma natural."
    )
    
    prompt_final = f"<bos><start_of_turn>user\nInstruccion: {instruccion_sistema}\n\nPregunta: {datos.prompt}<end_of_turn>\n<start_of_turn>model\n"
    payload = {"inputs": prompt_final, "parameters": {"max_new_tokens": 200, "temperature": 0.6, "return_full_text": False}}

    respuesta = requests.post(url, headers=headers_hf, json=payload)
    if respuesta.status_code == 200:
        texto_generado = respuesta.json().get("generated_text", "")
        return {"respuesta_ia": texto_generado.replace("<end_of_turn>", "").strip()}
    raise HTTPException(status_code=respuesta.status_code, detail="Error en la IA")
