import os
from typing import List, Dict, Any, Optional
import sqlite3
import secrets
from passlib.context import CryptContext
from repositories.users import register_user as repo_register_user
from repositories.users import get_user_by_email as repo_get_user_by_email
from repositories.users import list_all_users as repo_list_all_users
from repositories.users import get_user_statistics as repo_get_user_statistics
from repositories.users import create_user as repo_create_user
from repositories.users import update_user_role as repo_update_user_role
from repositories.users import get_user_photo_paths as repo_get_user_photo_paths
from repositories.users import delete_user as repo_delete_user
from repositories.users import update_user_name as repo_update_user_name
from repositories.users import get_user_rating_for_location as repo_get_user_rating_for_location
from repositories.users import rate_location as repo_rate_location

#Nastavení hashování na argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class UserService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def register_user(self, name: str, email: str, password: str) -> Dict[str, Any]:

        hashed_password = pwd_context.hash(password)
        #Ověření zda uživatel už není zaregistrován, auth provider je 1 - local
        new_id = repo_register_user(self.conn,name,email,hashed_password,1)
        if new_id is None:
            raise ValueError("Uživatel s tímto e-mailem již existuje.")

        return {
            "id": new_id,
            "name": name,
            "email": email
        }
    #Ověřuje jestli uživatel už není zaregistrovaný, potom případně vytvoří nového google usera
    def get_or_create_google_user(self, google_email: str, google_name: str) -> Dict[str, Any]:
        #Zkusíme najít uživatele
        user = repo_get_user_by_email(self.conn, google_email)

        if user:
            return user

        random_password = secrets.token_urlsafe(32)
        hashed_password = pwd_context.hash(random_password)
        #auth provider je 2 - google
        new_id = repo_register_user(self.conn, google_name, google_email, hashed_password, 2)

        if not new_id:
            raise ValueError("Chyba při vytváření Google uživatele")

        return {
            "id": new_id,
            "name": google_name,
            "email": google_email,
            "role": 3  # Default user
        }

    def create_user(self, name: str, email: str, password: str, role:int) -> Dict[str, Any]:
        hashed_password = pwd_context.hash(password)
        new_id = repo_create_user(self.conn, name, email, hashed_password, role)

        if new_id is None:
            raise ValueError("Uživatel s tímto e-mailem již existuje.")

        return {
            "id": new_id,
            "name": name,
            "email": email,
            "role": role
        }


    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        #Vytáhne usera z db
        user = repo_get_user_by_email(self.conn,email)

        if not user:
            return None  #Uživatel neexistuje
        #Porovná s hashem
        if not pwd_context.verify(password, user["password_hash"]):
            return None  #Špatné heslo

        #Success
        return user


    def list_all_users(self) -> List[Dict[str, Any]]:
        return repo_list_all_users(self.conn)

    def get_user_statistics(self, user_id: int) -> Dict[str, Any]:
        return repo_get_user_statistics(self.conn,user_id)

    def update_user_role(self, user_id: int, role_id: int) -> Optional[int]:
        return repo_update_user_role(self.conn,user_id,role_id)

    def delete_account(self, user_id: int):
        photo_urls = repo_get_user_photo_paths(self.conn, user_id)
        # Delete photos from physical
        for path in photo_urls:

            if os.path.exists(path):
                try:
                    os.remove(path)
                    print(f"Smazán soubor: {path}")

                    directory = os.path.dirname(path)
                    # Delete folder if empty
                    if not os.listdir(directory):
                        os.rmdir(directory)
                        print(f"Smazána prázdná složka: {directory}")
                except Exception as e:
                    print(f"Chyba při mazání souboru {path}: {e}")

        success = repo_delete_user(self.conn, user_id)
        if not success:
            raise ValueError("Nepodařilo se smazat účet z databáze.")

    def update_user_name(self, user_id: int, name: str) -> bool:
        return repo_update_user_name(self.conn,user_id,name)

    def get_user_rating_for_location(self, location_id: int, stars: int) -> Optional[int]:
        return repo_get_user_rating_for_location(self.conn,location_id,stars)
    def rate_location(self, location_id: int,user_id:int, stars: int) -> Optional[int]:
        return repo_rate_location(self.conn,location_id,user_id, stars)