from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio

app = FastAPI()

class Estado:
    def __init__(self):
        self.valor = 0

estado = Estado()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Status do Objeto</title>
</head>
<body>
    <h1>Valor atual: <span id="valor">Aguardando...</span></h1>
    <script>
        let ws = new WebSocket("ws://localhost:8000/ws");
        ws.onmessage = function(event) {
            document.getElementById("valor").innerText = event.data;
        };
    </script>
</body>
</html>
"""

html2 = """
<!DOCTYPE html>
<html>
<head>
    <title>Status do Objeto</title>
</head>
<body>
    <h1>Ops! Outra página.</h1>

</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/2")
async def get():
    return HTMLResponse(html2)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("abc...")
    while True:
        await asyncio.sleep(5)
        estado.valor += 1  # Simulação de mudança no estado
        await websocket.send_text(str(estado.valor))
