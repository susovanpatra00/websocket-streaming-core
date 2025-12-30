from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json
import time
import uuid

from .session import SessionState
from .sender import sender
from .heartbeat import heartbeat


async def websocket_handler(ws: WebSocket):
    await ws.accept()
    session = SessionState(session_id=str(uuid.uuid4()))

    print(f"Session connected: {session.session_id}")

    # background tasks
    sender_task = asyncio.create_task(sender(ws, session))
    heartbeat_task = asyncio.create_task(heartbeat(ws, session))

    try:
        while True:
            message = await ws.receive()

            # --------------------
            # TEXT FRAME
            # --------------------
            if "text" in message:
                data = json.loads(message["text"])
                msg_type = data.get("type")

                if msg_type == "pong":
                    session.last_pong_at = time.time()
                    continue

                if msg_type == "text":
                    # 👇 BACKPRESSURE APPLIED HERE
                    await session.send_queue.put(
                        json.dumps({
                            "type": "ack",
                            "id": data.get("id")
                        })
                    )

                if msg_type == "start_audio":
                    print("Audio stream started")

                if msg_type == "end_audio":
                    print("Audio stream ended")

            # --------------------
            # BINARY FRAME (audio)
            # --------------------
            elif "bytes" in message:
                audio_chunk = message["bytes"]

                # backpressure for audio too (optional)
                # await session.audio_queue.put(audio_chunk)
                print(f"Received audio chunk: {len(audio_chunk)} bytes")

    except WebSocketDisconnect:
        print(f"Client disconnected: {session.session_id}")

    finally:
        session.closed = True
        sender_task.cancel()
        heartbeat_task.cancel()
        print(f"Session cleaned: {session.session_id}")
