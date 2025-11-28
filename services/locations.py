import sqlite3
from typing import List, Dict, Any, Optional

from repositories.locations import list_locations as repo_list_locations
from repositories.locations import list_locations_with_photos_and_rating as repo_list_locations_with_photos_and_rating
from repositories.locations import get_location_by_id_with_photos_and_rating as repo_get_location_by_id_with_photos_and_rating
from repositories.locations import get_five_random_locations as repo_get_five_random_locations
from repositories.locations import get_most_favorite_location as repo_get_most_favorite_location
from repositories.locations import get_newest_location as repo_get_newest_location
from repositories.locations import list_locations_by_newest as repo_list_locations_by_newest
from repositories.locations import list_locations_by_avg_rating as repo_list_locations_by_avg_rating
from repositories.locations import list_locations_by_most_comments as repo_list_locations_by_most_comments
from repositories.locations import list_locations_added_by_concrete_user as repo_list_locations_added_by_concrete_user
from repositories.locations import add_location_to_favorites as repo_add_location_to_favorites
from repositories.locations import add_location_to_visited as repo_add_location_to_visited
from repositories.locations import is_location_visited as repo_is_location_visited
from repositories.locations import is_location_favorite as repo_is_location_favorite
from repositories.locations import remove_location_from_visited as repo_remove_location_from_visited
from repositories.locations import remove_location_from_favorite as repo_remove_location_from_favorite
from repositories.locations import list_comments as repo_list_comments
from repositories.locations import add_comment_to_location as repo_add_comment_to_location
from repositories.locations import remove_my_comment_from_location as repo_remove_my_comment_from_location
from repositories.locations import list_my_visited_locations as repo_list_my_visited_locations
from repositories.locations import list_my_favorite_locations as repo_list_my_favorite_locations
from repositories.locations import list_my_locations_with_pending_status as repo_list_my_locations_with_pending_status
from repositories.locations import list_pending_locations as repo_list_pending_locations
from repositories.locations import get_pending_location_detail as repo_get_pending_location_detail

class LocationService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def list_locations(self) -> List[Dict[str, Any]]:
        return repo_list_locations(self.conn)

    def list_locations_with_photos_rating(self) -> List[Dict[str, Any]]:
        return repo_list_locations_with_photos_and_rating(self.conn)

    def get_location_by_id_with_photos_and_rating(self, location_id: int) -> Dict[str, Any]:
        return repo_get_location_by_id_with_photos_and_rating(self.conn, location_id)

    def get_five_random_locations(self) -> List[Dict[str, Any]]:
        return repo_get_five_random_locations(self.conn)

    def get_most_favorite_location(self) -> Dict[str, Any]:
        return repo_get_most_favorite_location(self.conn)

    def get_newest_location(self) -> Dict[str, Any]:
        return repo_get_newest_location(self.conn)

    def list_locations_by_newest(self) -> List[Dict[str, Any]]:
        return repo_list_locations_by_newest(self.conn)

    def list_locations_by_avg_rating(self) -> List[Dict[str, Any]]:
        return repo_list_locations_by_avg_rating(self.conn)

    def list_locations_by_most_comments(self) -> List[Dict[str, Any]]:
        return repo_list_locations_by_most_comments(self.conn)

    def list_locations_added_by_concrete_user(self, id_user: int) -> List[Dict[str, Any]]:
        return repo_list_locations_added_by_concrete_user(self.conn, id_user)

    def add_location_to_favorite(self, id_user: int, id_location: int) -> Optional[int]:
        return repo_add_location_to_favorites(self.conn, id_user, id_location)

    def add_location_to_visited(self, id_user: int, id_location: int) -> Optional[int]:
        return repo_add_location_to_visited(self.conn, id_user, id_location)

    def get_user_interaction_status(self, user_id: int, location_id: int):
        return {
            "is_favorite": repo_is_location_favorite(self.conn, user_id, location_id),
            "is_visited": repo_is_location_visited(self.conn, user_id, location_id)
        }

    def remove_location_from_visited(self, id_user: int, id_location: int) -> Optional[int]:
        return repo_remove_location_from_visited(self.conn, id_user, id_location)

    def remove_location_from_favorite(self, id_user: int, id_location: int) -> Optional[int]:
        return repo_remove_location_from_favorite(self.conn, id_user, id_location)

    def add_comment_to_location(self, id_user: int, id_location: int, comment_text: str) -> Optional[int]:
        return repo_add_comment_to_location(self.conn, id_user, id_location, comment_text)

    def remove_my_comment_from_location(self, id_user: int, id_location: int) -> Optional[int]:
        return repo_remove_my_comment_from_location(self.conn, id_user, id_location)

    def list_comments(self, id_location: int) -> List[Dict[str, Any]]:
        return repo_list_comments(self.conn, id_location)

    def list_my_favorite_locations(self, user_id: int) -> List[Dict[str, Any]]:
        return repo_list_my_favorite_locations(self.conn, user_id)

    def list_my_visited_locations(self, user_id: int) -> List[Dict[str, Any]]:
        return repo_list_my_visited_locations(self.conn, user_id)

    def list_my_locations_with_pending_status(self, user_id: int) -> List[Dict[str, Any]]:
        return repo_list_my_locations_with_pending_status(self.conn, user_id)

    def list_pending_locations(self) -> List[Dict[str, Any]]:
        return repo_list_pending_locations(self.conn)

    def get_pending_location_detail(self, location_id: int) -> Dict[str, Any]:
        return repo_get_pending_location_detail(self.conn, location_id)
