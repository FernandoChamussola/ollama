FROM python:3.10-slim

WORKDIR /app

# dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# código
COPY app/ ./app

# instalar Ollama dentro do container
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://ollama.com/install.sh | sh

EXPOSE 8000

CMD ollama serve & \
    sleep 5 && \
    ollama pull gemma2:2b && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000