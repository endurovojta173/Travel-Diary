from typing import List, Dict, Any, Optional
import sqlite3


def register_user(conn: sqlite3.Connection, name:str, email:str, password_hash:str) -> Optional[int]:
    cursor = conn.cursor()
    try:
        #??? jsou ochrana proti sql injection, 3 je user role
        cursor.execute("""
                       INSERT INTO user (name, email, password_hash, id_role)
                       VALUES (?, ?, ?, ?) 
                       """, (name, email, password_hash, 3))

        conn.commit()
    except sqlite3.IntegrityError:

        return None

def create_user(conn: sqlite3.Connection, name:str, email:str, password_hash:str, role:int) -> Optional[int]:
    cursor = conn.cursor()
    try:
        #??? jsou ochrana proti sql injection, 3 je user role
        cursor.execute("""
                       INSERT INTO user (name, email, password_hash, id_role)
                       VALUES (?, ?, ?, ?) 
                       """, (name, email, password_hash, role))

        conn.commit()
    except sqlite3.IntegrityError:

        return None


def get_user_by_email(conn: sqlite3.Connection, email: str) -> Optional[Dict[str, Any]]:
    cursor = conn.cursor()
    # Vybereme id, jméno, heslo a roli
    cursor.execute("""
                   SELECT id, name, email, password_hash, id_role
                   FROM user
                   WHERE email = ?
                   """, (email,))

    row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "password_hash": row[3],
        "id_role": row[4]
    }

def list_all_users(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT id, name, email, id_role
                    FROM user
                   """)
    users = []

    for row in cursor.fetchall():
        user_data = {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "role": row[3]
        }

        users.append(user_data)

    return users


def get_user_statistics(conn: sqlite3.Connection, user_id: int) -> Dict[str, int]:
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT (SELECT COUNT(id) FROM location WHERE id_user = :uid)                  AS added_count,
                          (SELECT COUNT(*) FROM visited_location WHERE id_user = :uid)           AS visited_count,
                          (SELECT COUNT(DISTINCT id_location) FROM rating WHERE id_user = :uid)  AS rated_count,
                          (SELECT COUNT(DISTINCT id_location) FROM comment WHERE id_user = :uid) AS commented_count
                   """, {"uid": user_id})

    row = cursor.fetchone()
    if not row:
        return {"added": 0, "visited": 0, "rated": 0, "commented": 0}

    return {
        "added": row[0],
        "visited": row[1],
        "rated": row[2],
        "commented": row[3]
    }

def update_user_role(conn: sqlite3.Connection, user_id: int, role_id: int) -> Optional[int]:

    cursor = conn.cursor()
    try:
        cursor.execute("""
                       UPDATE user
                       SET id_role = ?
                       WHERE id = ?
                       """, (role_id, user_id))
        conn.commit()
        return True
    except:
        conn.rollback()
        return None

