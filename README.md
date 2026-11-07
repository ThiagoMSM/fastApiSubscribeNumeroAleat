# Random Number Streamer (FastAPI)

Serviço standalone em Python (FastAPI) que gera e emite números aleatórios de 30 dígitos continuamente através de **HTTP Streaming** (NDJSON e Server-Sent Events - SSE).

---

## 🚀 Como Iniciar o Servidor

O ambiente virtual `.venv` já está configurado com todas as dependências (`fastapi`, `uvicorn`, `httpx`).

Basta executar o script de inicialização:

```bash
./run.sh
```

Ou manualmente:
```bash
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

O servidor estará disponível em: `http://127.0.0.1:8000`  
Documentação interativa Swagger: `http://127.0.0.1:8000/docs`

---

## 📡 Endpoints de Streaming

### 1. `/stream/sse` (Server-Sent Events)
* **Formato:** `text/event-stream`
* **Ideal para:** Apidog, Postman (EventStream UI) e navegadores (EventSource).
* **Exemplo de URL:**
  ```text
  http://127.0.0.1:8000/stream/sse?duration=120&interval=1.0&digits=30
  ```

### 2. `/stream` (NDJSON / Chunked)
* **Formato:** `application/x-ndjson` (cada linha é um JSON independente).
* **Ideal para:** Consumo linha a linha via scripts, pipelines e `curl`.
* **Exemplo de URL:**
  ```text
  http://127.0.0.1:8000/stream?duration=120&interval=1.0&digits=30
  ```

### Parâmetros Query
| Parâmetro | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `duration` | float | `120.0` | Duração do streaming em **minutos** (ex: 120 = 2 horas). |
| `interval` | float | `1.0` | Intervalo em **segundos** entre cada envio (ex: 0.5, 1.0). |
| `digits` | int | `30` | Quantidade de dígitos do número gerado. |

---

## 🧪 Como Testar

### No Apidog:
1. Crie uma requisição `GET`.
2. URL: `http://127.0.0.1:8000/stream/sse?duration=120&interval=1`
3. Clique em **Send**. A resposta será exibida continuamente no painel de eventos.
4. Para parar, basta clicar em **Cancel**.

### No Terminal (via script cliente):
```bash
.venv/bin/python test_client.py
```

### No Terminal (via `curl`):
```bash
curl -N "http://127.0.0.1:8000/stream?duration=5&interval=0.5"
```

---

