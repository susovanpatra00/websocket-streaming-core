import asyncio

async def sender(ws, session):
    try:
        while True:
            message = await session.send_queue.get()
            await ws.send(message)
    except asyncio.CancelledError:
        pass
