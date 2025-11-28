from typing import List, Dict, Any, Optional
import sqlite3
from fastapi import HTTPException, status
from passlib.context import CryptContext
from repositories.users import register_user as repo_register_user
from repositories.users import get_user_by_email as repo_get_user_by_email
from repositories.users import list_all_users as repo_list_all_users

#Nastavení hashování na argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class UserService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def register_user(self, name: str, email: str, password: str) -> Dict[str, Any]:

        hashed_password = pwd_context.hash(password)
        #Ověření zda uživatel už není zaregistrován
        new_id = repo_register_user(self.conn,name,email,hashed_password)
        if new_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uživatel s tímto e-mailem již existuje."
            )

        return {
            "id": new_id,
            "name": name,
            "email": email
        }

        # Do třídy UserService přidej metodu:

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