"""Causes all Tables to register with the base model, by importing all
the table classes. You just need to import this module for it to work."""

from ..db import Base

from . import (
    task,
    report,
    ws,
    utility,
)

__all__ = [
    "Base",
    "task",
    "report",
    "ws",
    "utility"
]
