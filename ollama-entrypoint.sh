#!/bin/sh

echo "🚀 Iniciando Ollama..."
ollama serve &

# Espera o servidor subir
sleep 5

echo "🔍 Verificando modelo gemma2:2b..."

if ollama list | grep -q "gemma2:2b"; then
    echo "✅ Modelo já existe, usando cache do volume"
else
    echo "⬇️ Modelo não encontrado, baixando..."
    ollama pull gemma2:2b
    echo "✅ Download concluído"
fi

# Mantém container ativo
wait