from typing import List, Dict, Any, Optional
import sqlite3


def register_user(conn: sqlite3.Connection, name:str, email:str, password_hash:str,auth_provider_id:int) -> Optional[int]:
    cursor = conn.cursor()
    try:
        #??? jsou ochrana proti sql injection, 3 je user role
        cursor.execute("""
                       INSERT INTO user (name, email, password_hash, id_role, id_auth_provider)
                       VALUES (?, ?, ?, ?,?) 
                       """, (name, email, password_hash, 3, auth_provider_id))

        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:

        return None

def create_user(conn: sqlite3.Connection, name:str, email:str, password_hash:str, role:int) -> Optional[int]:
    cursor = conn.cursor()
    try:
        #??? jsou ochrana proti sql injection, 3 je user role
        cursor.execute("""
                       INSERT INTO user (name, email, password_hash, id_role, id_auth_provider)
                       VALUES (?, ?, ?, ?, ?) 
                       """, (name, email, password_hash, role, 1))

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
    except sqlite3.Error as e:
        print(e)
        conn.rollback()
        return None


def get_user_photo_paths(conn: sqlite3.Connection, user_id: int) -> List[str]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT p.url
                   FROM photo p
                            JOIN location l ON p.id_location = l.id
                   WHERE l.id_user = ?
                   """, (user_id,))

    # Vrátí seznam: ['img/locations/uuid/1.webp', 'img/locations/uuid/2.webp']
    return [row[0] for row in cursor.fetchall()]

def delete_user(conn: sqlite3.Connection, user_id: int) -> bool:
    cursor = conn.cursor()
    try:
        # Pokud máš v DB nastavené cizí klíče s ON DELETE CASCADE
        cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Chyba při mazání uživatele: {e}")
        conn.rollback()
        return False

def update_user_name(conn: sqlite3.Connection, user_id: int, name: str) -> bool:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       UPDATE user
                       SET name = ?
                       WHERE id = ?
                    """, (name, user_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        conn.rollback()
        return False

def get_user_rating_for_location(conn: sqlite3.Connection, location_id: int, user_id) -> Optional[int]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT rating
                   FROM rating
                   WHERE id_location = ?
                     AND id_user = ?
                   """, (location_id, user_id))
    row = cursor.fetchone()
    if row is None:
        return 0  # Uživatel ještě nehlasoval 0

    return row[0]

def rate_location(conn: sqlite3.Connection, location_id: int, user_id: int, rating:int) -> Optional[int]:
        cursor = conn.cursor()
        try:
            # Uživatel tuto lokaci hodnotil
            cursor.execute("""
                           SELECT 1
                           FROM rating
                           WHERE id_user = ?
                             AND id_location = ?
                           """, (user_id, location_id))

            exists = cursor.fetchone()

            if exists:
                cursor.execute("""
                               UPDATE rating
                               SET rating = ?
                               WHERE id_user = ?
                                 AND id_location = ?
                               """, (rating, user_id, location_id))
            else:
                cursor.execute("""
                               INSERT INTO rating (id_user, id_location, rating)
                               VALUES (?, ?, ?)
                               """, (user_id, location_id, rating))
            conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"Chyba při hodnocení: {e}")
            conn.rollback()
            return False