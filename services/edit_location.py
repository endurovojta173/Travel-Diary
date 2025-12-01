import sqlite3
from typing import List, Optional
from repositories.edit_location import update_location_details as repo_update_location_details

class EditLocationService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def update_location_details(self, location_id:int ,name:str, description:str ) -> Optional[dict]:
        return repo_update_location_details(self.conn, location_id, name, description)
