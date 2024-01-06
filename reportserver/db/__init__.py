from tortoise import BaseDBAsyncClient as DBClientConnection

memdb = {}

__all__ = [
    "DBClientConnection",
    "ConnectionName",
    "AppName",
    "AppModule",
    "DBSettings",
]
