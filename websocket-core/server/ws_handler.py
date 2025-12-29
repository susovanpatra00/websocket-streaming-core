from fastapi import WebSocket, WebSocketDisconnect
import json
import time
import uuid
from .session import SessionState

async def websocket_handler(ws: WebSocket):
    await ws.accept()
    session = SessionState(session_id=str(uuid.uuid4()))

    try:
        while True:
            raw = await ws.receive_text()
            session.last_message_at = time.time()

            message = json.loads(raw)

            if "type" not in message:
                await ws.send_text(json.dumps({
                    "type": "error",
                    "message": "Missing message type"
                }))
                continue

            if message["type"] == "text":
                await ws.send_text(json.dumps({
                    "type": "ack",
                    "id": message.get("id")
                }))

    except WebSocketDisconnect:
        # NORMAL client disconnect
        session.closed = True
        print(f"Client disconnected normally: {session.session_id}")

    except Exception as e:
        # REAL errors
        session.closed = True
        print("Unexpected error:", e)
