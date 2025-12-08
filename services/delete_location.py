import sqlite3
import os
from repositories.delete_location import delete_location as repo_delete_location

class DeleteLocationService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def delete_location_process(self, location_id: int):
        files_to_delete = repo_delete_location(self.conn, location_id)

        for file_path in files_to_delete:
            try:
                clean_path = file_path.lstrip("/")

                if os.path.exists(clean_path):
                    os.remove(clean_path)
                    print(f"SERVICE: Smazán soubor {clean_path}")

            except Exception as e:
                print(f"SERVICE ERROR: Nepodařilo se smazat soubor {file_path}: {e}")