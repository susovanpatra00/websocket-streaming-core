# WebSocket Streaming Core

This repo is my hands-on learning journey of **WebSockets**, focused on **real-time streaming use cases** (not just basic chat examples).

I already knew the theory of WebSockets, but this repo is about **actually implementing them**, understanding what breaks, and why certain patterns are needed in production systems (like voice agents).

---

### 1. Basic WebSocket connection

* FastAPI WebSocket server
* Python client using `websockets`
* Simple text message → ACK response
* Proper connection open and close handling

This helped me understand:

* WebSocket handshake
* Normal vs abnormal disconnects
* Why `WebSocketDisconnect` is not an error

---

### 2. Async & await (practical understanding)

* Learned that `await` is used only when something can **wait** (network, socket, sleep)
* Understood that WebSockets are mostly waiting, so async is mandatory
* Saw how one server can handle many clients without threads

---

### 3. Heartbeat (ping / pong)

* Implemented application-level heartbeat
* Server sends periodic `ping`
* Client responds with `pong`
* Server closes connection if client becomes unresponsive

Learned:

* Why heartbeat is needed for long-lived connections
* Why timeouts should not start before the first pong
* Async race conditions during startup

---

### 4. Binary frames (audio streaming basics)

* Used WebSocket binary frames to send audio chunks
* Mixed text (JSON control messages) and binary data
* Simulated real-time audio using chunking and sleep

Learned:

* Audio streaming is about **small chunks**, not files
* `ws.receive()` is required to handle both text and binary
* Real-time pacing matters

---

### 5. Backpressure (very important)

* Implemented a **send queue** using `asyncio.Queue`
* Created a dedicated sender task
* Ensured only one coroutine ever calls `ws.send_text()`

Learned:

* Why directly calling `ws.send()` everywhere is dangerous
* How backpressure prevents memory issues
* How slow clients should naturally slow the server
* Producer–consumer pattern in async systems

---

### 6. Partial / streaming text responses

* Implemented token-like streaming (`partial` messages)
* Sent final message after streaming completes
* Client assembles partial responses in real time

This is similar to how:

* LLM streaming works
* Streaming ASR responses work
* Voice agents stream responses instead of waiting for full output

---
