from typing import Optional
import sqlite3


def approve_location(conn: sqlite3.Connection, location_id) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       UPDATE location
                       SET id_status = 1
                       WHERE id = ?
                       """, (location_id,))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"Error updating location {e}")
        conn.rollback()
        return None

def reject_location(conn: sqlite3.Connection, location_id) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       UPDATE location
                       SET id_status = 3
                       WHERE id = :location_id
                       """, (location_id,))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"Error updating location {e}")
        conn.rollback()
        return None
