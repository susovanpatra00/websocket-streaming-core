from fastapi import WebSocket, WebSocketDisconnect
import json
import uuid

async def websocket_handler(ws: WebSocket):
    await ws.accept()
    session_id = str(uuid.uuid4())

    print("Session:", session_id)

    try:
        while True:
            message = await ws.receive()

            # 🔴 DISCONNECT FRAME
            if message["type"] == "websocket.disconnect":
                print("Client disconnected")
                break

            # 🟢 TEXT FRAME
            if "text" in message:
                data = json.loads(message["text"])

                if data["type"] == "start_audio":
                    print("Audio stream started")

                elif data["type"] == "end_audio":
                    print("Audio stream ended")

            # 🔵 BINARY FRAME
            elif "bytes" in message:
                audio_chunk = message["bytes"]
                print(f"Received audio chunk: {len(audio_chunk)} bytes")

    except WebSocketDisconnect:
        print("Client disconnected (exception)")
