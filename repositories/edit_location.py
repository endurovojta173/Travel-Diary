from typing import Optional
import sqlite3


def update_location_details(conn: sqlite3.Connection, location_id: int, name: str, description: str) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       UPDATE location
                       SET name        = ?,
                           description = ?
                       WHERE id = ?
                       """, (name, description, location_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return None
