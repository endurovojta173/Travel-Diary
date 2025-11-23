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

def login_user(conn: sqlite3.Connection, email:str, password:str) -> Optional[int]:
    cursor = conn.cursor()
    