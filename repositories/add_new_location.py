from typing import List, Dict, Any, Optional
import sqlite3


def add_new_location(conn: sqlite3.Connection,id_user: int,name: str,description: str,photos: Optional[List[Dict[str, str]]] = None) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       INSERT INTO location(name, description, id_user, id_status)
                       VALUES (?, ?, ?, 2)
                       """, (name, description, id_user))
        new_location_id = cursor.lastrowid
        if photos:
            photos_data = []
            for photo in photos:
                photos_data.append((
                    photo.get('alt_text', name),
                    photo.get('alt_text', ''),
                    photo.get('url'),
                    new_location_id
                ))
            cursor.executemany("""
                               INSERT INTO photo (name, alt_text, url, id_location)
                               VALUES (?, ?, ?, ?)
                               """, photos_data)

        conn.commit()
        print(222222222222222222222222222222)
        return new_location_id

    except sqlite3.Error as e:
        print(33333333333333333333333333333333)
        print(f"Error adding new location: {e}")
        conn.rollback()
        return None