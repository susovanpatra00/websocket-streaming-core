from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json
import time
import uuid

from .session import SessionState
from .sender import sender
from .heartbeat import heartbeat


async def stream_text(session, message_id, text):
    """
    Simulates token-by-token streaming.
    """
    for chunk in text.split(" "):
        await asyncio.sleep(0.3)  # simulate model latency

        await session.send_queue.put(
            json.dumps({
                "type": "partial",
                "id": message_id,
                "delta": chunk + " "
            })
        )

    await session.send_queue.put(
        json.dumps({
            "type": "final",
            "id": message_id,
            "text": text
        })
    )


async def websocket_handler(ws: WebSocket):
    print("🔥 websocket_handler ENTERED")
    await ws.accept()
    session = SessionState(session_id=str(uuid.uuid4()))

    sender_task = asyncio.create_task(sender(ws, session))
    heartbeat_task = asyncio.create_task(heartbeat(ws, session))

    try:
        while True:
            message = await ws.receive()

            # -------- TEXT --------
            if "text" in message:
                data = json.loads(message["text"])
                msg_type = data.get("type")

                if msg_type == "pong":
                    session.last_pong_at = time.time()
                    continue

                if msg_type == "text":
                    message_id = data.get("id")

                    # start streaming in background
                    asyncio.create_task(
                        stream_text(
                            session,
                            message_id,
                            "Hello this is a streamed response"
                        )
                    )

            # -------- BINARY (audio) --------
            elif "bytes" in message:
                # audio chunk handling here
                pass

    except WebSocketDisconnect:
        print(f"Client disconnected: {session.session_id}")

    finally:
        session.closed = True
        sender_task.cancel()
        heartbeat_task.cancel()
