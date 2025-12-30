# server/heartbeat.py
import asyncio
import json
import time

PING_INTERVAL = 5
PING_TIMEOUT = 10

async def heartbeat(ws, session):
    try:
        while True:
            await asyncio.sleep(PING_INTERVAL)
            now = time.time()

            # enqueue ping (NOT send directly)
            await session.send_queue.put(
                json.dumps({
                    "type": "ping",
                    "ts": now
                })
            )

            if session.last_pong_at is None:
                continue

            if now - session.last_pong_at > PING_TIMEOUT:
                print("Heartbeat timeout, closing connection")
                await ws.close(code=1001)
                break

    except asyncio.CancelledError:
        pass
