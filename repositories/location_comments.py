from typing import List, Dict, Optional
import sqlite3

def list_comments(conn: sqlite3.Connection, id_location: int) -> List[Dict[str, str]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT c.id,
                          u.name,
                          c.comment_time,
                          c.text
                   FROM comment c
                            JOIN user u ON c.id_user = u.id
                   WHERE c.id_location = ?
                   ORDER BY c.id DESC
                   """, (id_location,))

    comments = []
    for row in cursor.fetchall():
        comments.append({
            "comment_id": row[0],
            "author": row[1],
            "date": row[2],
            "text": row[3],
        })

    return comments


def add_comment_to_location(conn: sqlite3.Connection, id_user: int, id_location: int, comment_text: str) -> Optional[
    int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       INSERT INTO comment(id_user, id_location, text)
                       VALUES (?, ?, ?)
                       """, (id_user, id_location, comment_text))
        conn.commit()
    except:
        print("Error adding comment to location")
        conn.rollback()


def remove_my_comment_from_location(conn: sqlite3.Connection, id_user: int, id_location: int) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       DELETE
                       FROM comment
                       WHERE id_user = ?
                         AND id_location = ?
                       """, (id_user, id_location))
        conn.commit()
    except:
        print("Error removing comment from location")
        conn.rollback()