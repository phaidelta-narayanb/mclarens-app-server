from fastapi import FastAPI

from . import views


def init_app(app: FastAPI):
    app.add_websocket_route("/ws", views.ws_channel_handler)
