from typing import List, Dict, Optional
import sqlite3

def list_comments(conn: sqlite3.Connection, id_location: int) -> List[Dict[str, str]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT c.id,
                          u.id,
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
            "id": row[0],
            "user_id": row[1],
            "author": row[2],
            "date": row[3],
            "text": row[4],
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


def remove_comment_from_location(conn: sqlite3.Connection, id_comment) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       DELETE
                       FROM comment
                       WHERE id = ?
                       """, (id_comment,))
        conn.commit()
    except:
        print("Error removing comment from location")
        conn.rollback()

