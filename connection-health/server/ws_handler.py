from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json
import time
import uuid
from .session import SessionState
from .heartbeat import heartbeat   

async def websocket_handler(ws: WebSocket):
    await ws.accept()
    session = SessionState(session_id=str(uuid.uuid4()))

    heartbeat_task = asyncio.create_task(heartbeat(ws, session))

    try:
        while True:
            raw = await ws.receive_text()
            session.last_message_at = time.time()

            message = json.loads(raw)

            msg_type = message.get("type")

            if msg_type == "pong":
                session.last_pong_at = time.time()
                continue


            if msg_type == "text":
                await ws.send_text(json.dumps({
                    "type": "ack",
                    "id": message.get("id")
                }))

    except WebSocketDisconnect:
        print(f"Client disconnected: {session.session_id}")

    finally:
        session.closed = True
        heartbeat_task.cancel()
