import uvicorn
from fastapi import FastAPI, WebSocket
from .ws_handler import websocket_handler

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_handler(websocket)

if __name__ == "__main__":
    print("Starting WebSocket server on ws://localhost:8001/ws")
    uvicorn.run(app, host="127.0.0.1", port=8001)
