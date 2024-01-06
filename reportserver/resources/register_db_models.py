"""Imports all database models for use in registering to ORM"""

from .task.models import DBWorkTask

__all__ = [
    "DBWorkTask",
]
