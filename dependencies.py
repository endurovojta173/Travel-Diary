import sqlite3
from typing import Iterator
from fastapi import Depends
from database.database import open_connection
from services.locations import LocationService
from services.users import UserService
from services.add_new_location import AddNewLocationService
from services.approve_location import ApproveLocationService


def get_conn() -> Iterator[sqlite3.Connection]:
    with open_connection() as conn:
        yield conn

def locations_service(conn: sqlite3.Connection = Depends(get_conn)) -> LocationService:
    return LocationService(conn)

def user_service(conn: sqlite3.Connection = Depends(get_conn)) -> UserService:
    return UserService(conn)

def add_new_location_service(conn: sqlite3.Connection = Depends(get_conn)) -> AddNewLocationService:
    return AddNewLocationService(conn)

def approve_location_service(conn: sqlite3.Connection = Depends(get_conn)) -> ApproveLocationService:
    return ApproveLocationService(conn)