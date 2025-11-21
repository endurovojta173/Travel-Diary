from typing import List, Dict, Any, Optional
import sqlite3
from repositories.locations import list_locations as repo_list_locations
from repositories.locations import list_locations_with_photos_and_rating as repo_list_locations_with_photos_and_rating

class LocationService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def list_locations(self) -> List[Dict[str, Any]]:
        return repo_list_locations(self.conn)

    def list_locations_with_photos_rating(self) -> List[Dict[str, Any]]:
        return repo_list_locations_with_photos_and_rating(self.conn)