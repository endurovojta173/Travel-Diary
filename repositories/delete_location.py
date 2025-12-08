from typing import List
import sqlite3


def delete_location(conn: sqlite3.Connection, location_id: int) -> List[str]:
    cursor = conn.cursor()

    cursor.execute("SELECT url FROM photo WHERE id_location = ?", (location_id,))
    photos = cursor.fetchall()

    photo_paths = [row[0] for row in photos]
    cursor.execute("DELETE FROM comment WHERE id_location = ?", (location_id,))
    cursor.execute("DELETE FROM rating WHERE id_location = ?", (location_id,))
    cursor.execute("DELETE FROM favorite_location WHERE id_location = ?", (location_id,))
    cursor.execute("DELETE FROM visited_location WHERE id_location = ?", (location_id,))
    cursor.execute("DELETE FROM photo WHERE id_location = ?", (location_id,))

    cursor.execute("DELETE FROM location WHERE id = ?", (location_id,))
    conn.commit()
    return photo_paths
