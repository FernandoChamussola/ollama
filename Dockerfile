FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Baixar e instalar Ollama manualmente
RUN curl -fsSL https://ollama.com/install.sh | sh

# Instalar dependências Python
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Código
COPY app ./app

EXPOSE 8000

CMD ollama serve & \
    sleep 10 && \
    ollama pull gemma2:2b && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000