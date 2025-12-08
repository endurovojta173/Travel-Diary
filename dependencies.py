import sqlite3
from typing import Iterator
from fastapi import Depends
from database.database import open_connection
from services.list_locations import LocationService
from services.users import UserService
from services.add_new_location import AddNewLocationService
from services.approve_location import ApproveLocationService
from services.location_comments import LocationCommentsService
from services.edit_location import EditLocationService
from services.delete_location import DeleteLocationService



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

def location_comments_service(conn: sqlite3.Connection = Depends(get_conn)) -> LocationCommentsService:
    return LocationCommentsService(conn)

def edit_location_service(conn: sqlite3.Connection = Depends(get_conn)) -> EditLocationService:
    return EditLocationService(conn)
def delete_location_service(conn: sqlite3.Connection = Depends(get_conn)) -> DeleteLocationService:
    return DeleteLocationService(conn)