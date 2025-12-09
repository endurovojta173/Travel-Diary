import sqlite3
import os
import uuid
from typing import List, Optional
from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError

from repositories.add_new_location import add_new_location as repo_add_new_location

class AddNewLocationService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def _prepare_upload_directory(self) -> tuple[str, str]:
        # Relativní cesta k projektu
        base_path = os.path.join("database", "img", "locations")

        while True:
            dir_uuid = str(uuid.uuid4())
            full_path = os.path.join(base_path, dir_uuid)

            if not os.path.exists(full_path):
                os.makedirs(full_path, exist_ok=True)
                return dir_uuid, full_path

    def add_new_location(self,location_name: str,location_description: str,id_user: int,files: List[UploadFile]) -> Optional[int]:

        dir_uuid, save_dir = self._prepare_upload_directory()
        photos_data_for_db = []

        if files:
            for file in files:
                if not file.filename:
                    continue

                try:
                    with Image.open(file.file) as img:
                        # Nový název + nová koncovka webp
                        filename = f"{uuid.uuid4()}.webp"
                        file_path_on_disk = os.path.join(save_dir, filename)

                        # Převed na WebP a uloží
                        img.save(file_path_on_disk, format="WEBP", quality=80, optimize=True)


                        web_url = f"database/img/locations/{dir_uuid}/{filename}"

                        photos_data_for_db.append({
                            "url": web_url,
                            "alt_text": location_name
                        })

                except UnidentifiedImageError:
                    print(f"Soubor {file.filename} není validní obrázek, přeskakuji.")
                    continue
                except Exception as e:
                    print(f"Chyba při ukládání {file.filename}: {e}")
                    continue
        return repo_add_new_location(
            self.conn,
            id_user,
            location_name,
            location_description,
            photos_data_for_db
        )
