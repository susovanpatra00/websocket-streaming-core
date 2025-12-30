import asyncio
import websockets
import json
import uuid
import time
from collections import defaultdict


async def main():
    print("🔥 client starting")
    async with websockets.connect("ws://127.0.0.1:8001/ws") as ws:
        print("🔥 client connected")
        msg_id = str(uuid.uuid4())

        await ws.send(json.dumps({
            "type": "text",
            "id": msg_id,
            "payload": {"text": "hi"}
        }))

        buffers = defaultdict(str)

        while True:
            msg = json.loads(await ws.recv())

            if msg["type"] == "ping":
                await ws.send(json.dumps({
                    "type": "pong",
                    "ts": time.time()
                }))

            elif msg["type"] == "partial":
                buffers[msg["id"]] += msg["delta"]
                print("\rStreaming:", buffers[msg["id"]], end="", flush=True)

            elif msg["type"] == "final":
                print("\nFinal:", msg["text"])
                buffers.pop(msg["id"], None)

if __name__ == "__main__":
    asyncio.run(main())


