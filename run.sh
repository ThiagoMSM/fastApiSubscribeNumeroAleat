#!/usr/bin/env bash
# Script para iniciar o servidor localmente
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "Iniciando o Random Number Streamer em http://127.0.0.1:8000"
echo "Documentação Swagger: http://127.0.0.1:8000/docs"
echo "Pressione Ctrl+C para encerrar."
echo ""

"$DIR/.venv/bin/uvicorn" main:app --host 0.0.0.0 --port 8000 --reload
