from typing import List, Dict, Any, Optional
import sqlite3
from repositories.locations import list_locations as repo_list_locations
from repositories.locations import list_locations_with_photos_and_rating as repo_list_locations_with_photos_and_rating
from repositories.locations import get_location_by_id_with_photos_and_rating as repo_get_location_by_id_with_photos_and_rating

class LocationService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def list_locations(self) -> List[Dict[str, Any]]:
        return repo_list_locations(self.conn)

    def list_locations_with_photos_rating(self) -> List[Dict[str, Any]]:
        return repo_list_locations_with_photos_and_rating(self.conn)

    def get_location_by_id_with_photos_and_rating(self, location_id: int) -> Dict[str, Any]:
        return repo_get_location_by_id_with_photos_and_rating(self.conn, location_id)