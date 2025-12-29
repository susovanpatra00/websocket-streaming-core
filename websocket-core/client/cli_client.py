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
            "timestamp": time.time(),
            "payload": {
                "text": "hello websocket"
            }
        }

        await ws.send(json.dumps(msg))
        print(await ws.recv())

asyncio.run(main())
