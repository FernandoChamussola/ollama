from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI(
    title="AI Log Analyzer",
    description="API para analisar logs usando Ollama",
    version="1.0.0"
)

# 🔹 URL do Ollama via variável de ambiente
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = "gemma2:2b"


class LogRequest(BaseModel):
    logs: str


@app.get("/")
def root():
    return {
        "message": "Bem-vindo ao AI Log Analyzer!",
        "usage": "Use POST /analyze com logs."
    }


def analyze(logs: str) -> str:
    prompt = f"""
Analisa estes logs e explica em linguagem simples o que aconteceu:

{logs}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Erro no Ollama: {response.text}"
            )

        data = response.json()

        if "response" not in data:
            raise HTTPException(
                status_code=500,
                detail="Resposta inválida do modelo"
            )

        return data["response"]

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Timeout ao comunicar com o modelo"
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar ao Ollama"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )


@app.post("/analyze")
def analyze_logs(req: LogRequest):
    if not req.logs.strip():
        raise HTTPException(
            status_code=400,
            detail="Logs não podem estar vazios"
        )

    result = analyze(req.logs)

    return {
        "status": "success",
        "analysis": result
    }