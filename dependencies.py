import sqlite3
from typing import Iterator
from fastapi import Depends
from database.database import open_connection
from services.locations import LocationService


def get_conn() -> Iterator[sqlite3.Connection]:
    with open_connection() as conn:
        yield conn

def locations_service(conn: sqlite3.Connection = Depends(get_conn)) -> LocationService:
    return LocationService(conn)
