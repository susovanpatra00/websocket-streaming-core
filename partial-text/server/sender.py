# server/sender.py
import asyncio

async def sender(ws, session):
    try:
        while True:
            message = await session.send_queue.get()
            await ws.send_text(message)   
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print("Sender crashed:", e)
