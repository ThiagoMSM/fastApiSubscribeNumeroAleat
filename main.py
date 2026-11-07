import asyncio
import json
import random
import time
from datetime import datetime, timezone
from fastapi import FastAPI, Query, Request
from fastapi.responses import StreamingResponse

app = FastAPI(
    title="Random Number Streamer",
    description="Serviço para emitir números de 30 dígitos continuamente via HTTP Streaming.",
    version="1.0.0"
)

def generate_random_digits(n: int = 30) -> str:
    """Gera uma string de n dígitos numéricos aleatórios."""
    # O primeiro dígito pode ser de 1-9 para não começar com zero caso queira tratar como número estrito,
    # ou 0-9 para sequência numérica pura. Usamos 1-9 no primeiro e 0-9 nos demais.
    first_digit = str(random.randint(1, 9))
    rest = ''.join([str(random.randint(0, 9)) for _ in range(n - 1)])
    return first_digit + rest

async def event_generator(
    request: Request,
    duration_minutes: float,
    interval_seconds: float,
    digits: int,
    is_sse: bool = False
):
    """
    Gera eventos continuamente até atingir a duração limite ou até o cliente desconectar.
    """
    end_time = time.time() + (duration_minutes * 60)
    counter = 0

    try:
        while time.time() < end_time:
            # Verifica se o cliente encerrou a conexão (ex: cancelou no Apidog)
            if await request.is_disconnected():
                break

            counter += 1
            num = generate_random_digits(digits)
            timestamp = datetime.now(timezone.utc).isoformat()
            
            data = {
                "sequence": counter,
                "number": num,
                "timestamp": timestamp
            }

            if is_sse:
                # Formato Server-Sent Events: data: <payload>\n\n
                yield f"id: {counter}\nevent: number\ndata: {json.dumps(data)}\n\n"
            else:
                # Formato NDJSON: cada linha é um JSON válido
                yield json.dumps(data) + "\n"

            await asyncio.sleep(interval_seconds)

    except asyncio.CancelledError:
        # Tratamento elegante quando o cliente encerra a chamada HTTP
        pass

@app.get("/")
def home():
    return {
        "status": "online",
        "description": "API de streaming de números aleatórios.",
        "endpoints": {
            "stream_ndjson": "/stream?duration=120&interval=1.0&digits=30",
            "stream_sse": "/stream/sse?duration=120&interval=1.0&digits=30"
        }
    }

@app.get("/stream")
async def stream_ndjson(
    request: Request,
    duration: float = Query(120.0, description="Duração do streaming em minutos (ex: 120 = 2 horas)"),
    interval: float = Query(1.0, description="Intervalo em segundos entre cada número (ex: 1.0, 0.5)"),
    digits: int = Query(30, description="Quantidade de dígitos por número (default: 30)")
):
    """
    Retorna um fluxo contínuo em formato NDJSON (Newline Delimited JSON).
    Ideal para ler linha por linha em ferramentas como Apidog, Postman ou scripts.
    """
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no"
    }
    return StreamingResponse(
        event_generator(request, duration, interval, digits, is_sse=False),
        media_type="application/x-ndjson",
        headers=headers
    )

@app.get("/stream/sse")
async def stream_sse(
    request: Request,
    duration: float = Query(120.0, description="Duração do streaming em minutos (ex: 120 = 2 horas)"),
    interval: float = Query(1.0, description="Intervalo em segundos entre cada número (ex: 1.0, 0.5)"),
    digits: int = Query(30, description="Quantidade de dígitos por número (default: 30)")
):
    """
    Retorna um fluxo contínuo no formato padrão SSE (Server-Sent Events: text/event-stream).
    O Apidog possui visualização em tempo real nativa para este formato.
    """
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no"
    }
    return StreamingResponse(
        event_generator(request, duration, interval, digits, is_sse=True),
        media_type="text/event-stream",
        headers=headers
    )
