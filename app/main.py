from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class LogRequest(BaseModel):
    logs: str

@app.get("/")
def root():
    return {"message": "Bem-vindo ao AI Log Analyzer! Use o endpoint /analyze para analisar logs."}

def analyze(logs):
    prompt = f"""
Analisa estes logs e explica em linguagem simples o que aconteceu:

{logs}
"""

    result = subprocess.run(
        ["ollama", "run", "gemma2:2b"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout


@app.post("/analyze")
def analyze_logs(req: LogRequest):
    return {"result": analyze(req.logs)}