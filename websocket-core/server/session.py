from dataclasses import dataclass, field
import time
from collections import deque

@dataclass
class SessionState:
    session_id: str
    connected_at: float = field(default_factory=time.time)
    last_message_at: float = field(default_factory=time.time)
    send_queue: deque = field(default_factory=deque)
    closed: bool = False
