from fastapi import WebSocket
from pydantic import BaseModel


class UpdateMessage(BaseModel):
    pass


async def ws_channel_handler(websocket: WebSocket):
    await websocket.accept()
    # TODO: Make it more sophisticated using pubsub
    # websocket.
