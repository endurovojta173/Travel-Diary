from typing import List, Dict, Any, Optional
import sqlite3

def list_locations(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    rows = conn.execute('SELECT * FROM Location').fetchall()
    return [dict(r) for r in rows]

def list_locations_with_photos(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    # SQL dotaz - LEFT JOIN, aby i lokace bez fotek byly vráceny
    cursor.execute("""
                   SELECT l.id          AS loc_id,
                          l.name        AS loc_name,
                          l.description AS loc_description,
                          p.id          AS photo_id,
                          p.name        AS photo_name,
                          p.alt_text    AS photo_alt_text,
                          p.url         AS photo_url
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                   ORDER BY l.id
                   """)
    #Inicializace slovníku
    locations: Dict[int, Dict[str, Any]] = {}

    for row in cursor.fetchall():
        loc_id = row[0]

        # pokud ještě není lokace přidána, vytvoříme ji, zajišťuje, aby se k lokaci dalo přiřadit více fotek a envytvářeli se nové lokace v dictu
        if loc_id not in locations:
            locations[loc_id] = {
                "id": loc_id,
                "name": row[1],
                "description": row[2],
                "photos": []
            }

        # pokud je přiřazená fotka, přidáme ji do seznamu
        if row[3] is not None:
            locations[loc_id]["photos"].append({
                "id": row[3],
                "name": row[4],
                "alt_text": row[5],
                "url": row[6]
            })

    return list(locations.values())

def list_locations_with_photos_and_rating(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()

    # SQL dotaz - LEFT JOIN pro fotky, subquery pro průměrné hodnocení
    cursor.execute("""
                   SELECT l.id          AS loc_id,
                          l.name        AS loc_name,
                          l.description AS loc_description,
                          p.id          AS photo_id,
                          p.name        AS photo_name,
                          p.alt_text    AS photo_alt_text,
                          p.url         AS photo_url,
                          r.avg_rating  AS avg_rating
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating
                                       FROM rating
                                       GROUP BY id_location) r ON l.id = r.id_location
                   ORDER BY l.id
                   """)

    # Inicializace slovníku
    locations: Dict[int, Dict[str, Any]] = {}

    for row in cursor.fetchall():
        loc_id = row[0]

        # pokud ještě není lokace přidána, vytvoříme ji
        if loc_id not in locations:
            locations[loc_id] = {
                "id": loc_id,
                "name": row[1],
                "description": row[2],
                "photos": [],
                "avg_rating": row[7]  # průměrné hodnocení
            }

        # pokud je přiřazená fotka, přidáme ji do seznamu
        if row[3] is not None:
            locations[loc_id]["photos"].append({
                "id": row[3],
                "name": row[4],
                "alt_text": row[5],
                "url": row[6]
            })

    return list(locations.values())