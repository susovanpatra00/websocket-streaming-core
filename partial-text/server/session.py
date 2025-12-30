from dataclasses import dataclass, field
import time
import asyncio

@dataclass
class SessionState:
    session_id: str
    connected_at: float = field(default_factory=time.time)
    last_message_at: float = field(default_factory=time.time)
    last_pong_at: float | None = None
    send_queue: asyncio.Queue = field(default_factory=lambda: asyncio.Queue(maxsize=50))
    closed: bool = False


