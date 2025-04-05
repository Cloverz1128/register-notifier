from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Request, Query
import asyncio
from typing import Optional

router = APIRouter()

sse_connections: list[asyncio.Queue] = [] # message queue for all connected users

class SSEBroadcaster:
    async def broadcast(self, event_type: str, data: str):
        message = {
            "id": None,
            "type": event_type,
            "data": data
        }
        for queue in sse_connections:
            await queue.put(message)

broadcaster = SSEBroadcaster()

async def sse_event_stream(queue: asyncio.Queue):
    try:
        while True:
            msg = await queue.get()
            yield (
                f"event: {msg['type']}\n"
                f"data: {msg['data']}\n\n"
            )
    except asyncio.CancelledError:
        pass  # logout

@router.get("/sse")
async def sse_endpoint(request: Request, last_event_id: Optional[int] = Query(None)):
    queue = asyncio.Queue()  # create new message queue for new user
    sse_connections.append(queue)
    async def event_stream():
        try:
            async for chunk in sse_event_stream(queue):
                yield chunk
        finally:
            sse_connections.remove(queue)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
