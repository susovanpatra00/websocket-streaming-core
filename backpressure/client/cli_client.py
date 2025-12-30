import asyncio
import websockets
import json
import uuid
import time


async def main():
    async with websockets.connect("ws://127.0.0.1:8001/ws") as ws:

        # send one text message
        await ws.send(json.dumps({
            "type": "text",
            "id": str(uuid.uuid4()),
            "payload": {"text": "hello websocket"}
        }))

        # keep reading forever
        while True:
            msg = json.loads(await ws.recv())

            if msg["type"] == "ping":
                await ws.send(json.dumps({
                    "type": "pong",
                    "ts": time.time()
                }))

            else:
                print("Received:", msg)


asyncio.run(main())
