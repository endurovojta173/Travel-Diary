import sqlite3
from typing import Optional
from repositories.approve_location import approve_location as repo_approve_location
from repositories.approve_location import reject_location as repo_reject_location

class ApproveLocationService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def approve_location(self, location_id: int) -> Optional[int]:
        return repo_approve_location(self.conn, location_id)

    def reject_location(self, location_id: int) -> Optional[int]:
        return repo_reject_location(self.conn, location_id)