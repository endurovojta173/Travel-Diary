import sqlite3
from typing import List, Dict, Any, Optional

from repositories.location_comments import list_comments as repo_list_comments
from repositories.location_comments import add_comment_to_location as repo_add_comment_to_location
from repositories.location_comments import remove_my_comment_from_location as repo_remove_my_comment_from_location


class LocationCommentsService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_comment_to_location(self, id_user: int, id_location: int, comment_text: str) -> Optional[int]:
        return repo_add_comment_to_location(self.conn, id_user, id_location, comment_text)

    def remove_my_comment_from_location(self, id_user: int, id_location: int) -> Optional[int]:
        return repo_remove_my_comment_from_location(self.conn, id_user, id_location)

    def list_comments(self, id_location: int) -> List[Dict[str, Any]]:
        return repo_list_comments(self.conn, id_location)
