FROM ollama/ollama:latest

WORKDIR /app

# instalar Python e pip
RUN apt-get update && apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# instalar dependências uma a uma para evitar erros
RUN pip3 install --no-cache-dir fastapi uvicorn pydantic

# código - cria pasta app/
COPY app ./app

EXPOSE 8000

CMD ollama serve & \
    sleep 5 && \
    ollama pull gemma2:2b && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000