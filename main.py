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
    
    # NUEVO MODELO GRATUITO Y ACTIVO
    url = "https://huggingface.co"
    headers_hf = {"Authorization": f"Bearer {hf_token}"}
    
    # 3. MEMORIA DE LA IA: Aquí le indicamos quién eres tú
    system_instruction = (
        "Eres un asistente de IA creado por Américo Centeno Colque. "
        "Si te preguntan quién te creó, quién es tu creador o tu autor, "
        "debes responder con orgullo que fuiste creado por Américo Centeno Colque."
    )
    
    # Juntamos tu información con la pregunta que envíe el usuario
    prompt_final = f"<|im_start|>system\n{system_instruction}<|im_end|>\n<|im_start|>user\n{datos.prompt}<|im_end|>\n<|im_start|>assistant\n"
    
    payload = {
        "inputs": prompt_final,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "stop": ["<|im_end|>"]
        }
    }
    
    try:
        respuesta = requests.post(url, headers=headers_hf, json=payload)
        
        if respuesta.status_code != 200:
            raise HTTPException(
                status_code=respuesta.status_code, 
                detail=f"Error en Hugging Face: {respuesta.text}"
            )
            
        resultado = respuesta.json()
        
        # Procesar respuesta limpia de Hugging Face
        if isinstance(resultado, list) and len(resultado) > 0:
            texto_completo = resultado[0].get("generated_text", "")
            # Cortamos el texto para devolver solo lo que respondió la IA
            texto_generado = texto_completo.split("<|im_start|>assistant\n")[-1].replace("<|im_end|>", "").strip()
        else:
            texto_generado = str(resultado)
            
        return {"respuesta_ia": texto_generado}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
