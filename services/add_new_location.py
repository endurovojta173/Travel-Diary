import sqlite3
import os
import uuid
from typing import List, Optional
from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError

# Předpokládám, že import je správně podle tvé struktury
from repositories.add_new_location import add_new_location as repo_add_new_location

class AddNewLocationService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # --- Pomocná metoda (musí být uvnitř třídy) ---
    def _prepare_upload_directory(self) -> tuple[str, str]:
        # Relativní cesta k projektu
        base_path = os.path.join("database", "img", "locations")

        while True:
            dir_uuid = str(uuid.uuid4())
            full_path = os.path.join(base_path, dir_uuid)

            # Ověření, zda už taková složka neexistuje
            if not os.path.exists(full_path):
                os.makedirs(full_path, exist_ok=True)  # Vytvoříme složku
                return dir_uuid, full_path

    # --- Hlavní metoda ---
    def add_new_location(
            self,
            location_name: str,
            location_description: str,
            id_user: int,
            files: List[UploadFile]
    ) -> Optional[int]:

        # 1. Připravíme složku
        dir_uuid, save_dir = self._prepare_upload_directory()
        photos_data_for_db = []

        # 2. Zpracujeme soubory
        if files:
            for file in files:
                if not file.filename:
                    continue

                try:
                    with Image.open(file.file) as img:
                        # Nový název + nová koncovka webp
                        filename = f"{uuid.uuid4()}.webp"
                        file_path_on_disk = os.path.join(save_dir, filename)

                        # Převedeme na WebP a uložíme
                        img.save(file_path_on_disk, format="WEBP", quality=80, optimize=True)

                        # Nová URL pro databázi
                        # Poznámka: Zkontroluj si, jestli tu chceš 'database/' na začátku.
                        # Pokud máš mount na '/database', tak je to OK.
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

        # 3. Až po zpracování VŠECH fotek voláme repozitář (TOTO MUSÍ BÝT MIMO CYKLUS)
        return repo_add_new_location(
            self.conn,
            id_user,
            location_name,
            location_description,
            photos_data_for_db
        )
