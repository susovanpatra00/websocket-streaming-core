import asyncio
import websockets
import json
import time
import os

CHUNK_SIZE = 640  # 20ms PCM16 @ 16kHz

async def main():
    async with websockets.connect("ws://127.0.0.1:8001/ws") as ws:

        # tell server audio is starting
        await ws.send(json.dumps({
            "type": "start_audio",
            "codec": "pcm16",
            "sr": 16000
        }))

        # fake audio stream
        for _ in range(50):
            fake_audio = os.urandom(CHUNK_SIZE)
            await ws.send(fake_audio)
            await asyncio.sleep(0.02)  # real-time pacing

        # tell server audio ended
        await ws.send(json.dumps({
            "type": "end_audio"
        }))

asyncio.run(main())
