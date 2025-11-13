import sqlite3
from typing import Iterator
from fastapi import Depends
from database.database import open_connection
from services.items import ItemsService

def get_conn() -> Iterator[sqlite3.Connection]:
    with open_connection() as conn:
        yield conn

def items_service(conn: sqlite3.Connection = Depends(get_conn)) -> ItemsService:
    return ItemsService(conn)
