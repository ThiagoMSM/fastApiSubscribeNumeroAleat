#!/usr/bin/env python3
"""
Script cliente simples para consumir o stream via terminal.
"""
import sys
import httpx

URL = "http://127.0.0.1:8000/stream?duration=1&interval=0.5&digits=30"

print(f"Conectando ao stream: {URL}")
print("Pressione Ctrl+C para parar a qualquer momento.\n")

try:
    with httpx.stream("GET", URL, timeout=None) as response:
        for line in response.iter_lines():
            if line:
                print(f"[Recebido] {line}")
except KeyboardInterrupt:
    print("\nConexão encerrada pelo usuário.")
except Exception as e:
    print(f"\nErro de conexão (o servidor está rodando?): {e}")
