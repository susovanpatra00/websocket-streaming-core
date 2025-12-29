import asyncio
import json
import time

PING_INTERVAL = 5       # seconds
PING_TIMEOUT = 10       # seconds
async def heartbeat(ws, session):
    try:
        while True:
            await asyncio.sleep(PING_INTERVAL)

            now = time.time()

            # send ping
            await ws.send_text(json.dumps({
                "type": "ping",
                "ts": now
            }))

            # 🚨 only enforce timeout AFTER first pong
            if session.last_pong_at is None:
                continue

            if now - session.last_pong_at > PING_TIMEOUT:
                print("Heartbeat timeout, closing connection")
                await ws.close(code=1001)
                break

    except asyncio.CancelledError:
        pass
    except Exception:
        pass
