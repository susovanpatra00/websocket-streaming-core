import asyncio
import websockets
import json
import uuid
import time

async def main():
    async with websockets.connect("ws://127.0.0.1:8001/ws") as ws:

        msg = {
            "type": "text",
            "id": str(uuid.uuid4()),
            "payload": {"text": "hello websocket"}
        }

        await ws.send(json.dumps(msg))

        while True:
            msg = json.loads(await ws.recv())

            if msg["type"] == "ping":
                await ws.send(json.dumps({
                    "type": "pong",
                    "ts": time.time()
                }))

            else:
                print(msg)

asyncio.run(main())
