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

        #ID nově vytvořeného uživatele (hodí se pro automatické přihlášení)
        #return cursor.lastrowid
    #Email nastaven jako unique, takže to při kolizi navrátí none
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
            "id_role": row[3]
        }

        users.append(user_data)

    return users