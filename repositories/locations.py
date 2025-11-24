from typing import List, Dict, Any
import sqlite3

def list_locations(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    rows = conn.execute('SELECT * FROM Location').fetchall()
    return [dict(r) for r in rows]


def list_locations_with_photos_and_rating(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()

    # SQL dotaz - LEFT JOIN pro fotky, subquery pro průměrné hodnocení
    cursor.execute("""
                   SELECT l.id          AS loc_id,
                          l.name        AS loc_name,
                          l.description AS loc_description,
                          l.status      AS loc_status,
                          p.id          AS photo_id,
                          p.alt_text    AS photo_alt_text,
                          p.url         AS photo_url,
                          r.avg_rating  AS avg_rating
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating
                                       FROM rating
                                       GROUP BY id_location) r ON l.id = r.id_location
                    WHERE l.status = 'approved'
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
        if row[4] is not None:
            locations[loc_id]["photos"].append({
                "id": row[4],
                "alt_text": row[5],
                "url": row[6]
            })

    return list(locations.values())

def get_location_by_id_with_photos_and_rating(conn: sqlite3.Connection, location_id:int) -> Dict[str, Any]:
    cursor = conn.cursor()
    # SQL
    cursor.execute("""
                   SELECT l.id          AS loc_id,
                          l.name        AS loc_name,
                          l.description AS loc_description,
                          l.date_location_added AS loc_date_location_added,
                          p.id          AS photo_id,
                          p.alt_text    AS photo_alt_text,
                          p.url         AS photo_url,
                          r.avg_rating  AS avg_rating
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating
                                       FROM rating
                                       GROUP BY id_location) r ON l.id = r.id_location
                   WHERE l.id = :id AND l.status = 'approved'
                   ORDER BY l.id
                   """, {"id": location_id})

    #Inicializace slovníku
    location = {}

    for row in cursor.fetchall():
        location = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "date_location_added": row[3],
            "photos": [],
            "avg_rating": row[7]
        }

        # pokud je přiřazená fotka, přidáme ji do seznamu
        if row[4] is not None:
            location["photos"].append({
                "id": row[4],
                "alt_text": row[5],
                "url": row[6]
            })

    return location

def get_five_random_locations(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    #Vybere 5 random lokací
    cursor.execute("""
                   SELECT l.id       AS loc_id,
                          l.name     AS loc_name,
                          p.id       AS photo_id,
                          p.alt_text AS photo_alt_text,
                          p.url      AS photo_url
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                    WHERE l.status = 'approved'
                   GROUP BY l.id
                   ORDER BY RANDOM()
                   LIMIT 5
                   """)

    locations = []

    for row in cursor.fetchall():
        loc_data = {
            "id": row[0],
            "name": row[1],
            "photo": None
        }

        if row[2] is not None:
            loc_data["photo"] = {
                "id": row[2],
                "alt_text": row[3],
                "url": row[4]
            }

        locations.append(loc_data)

    return locations

def get_most_favorite_location(conn: sqlite3.Connection) -> Dict[str, Any]:
    cursor = conn.cursor()
    # SQL
    cursor.execute("""
                   SELECT l.id                  AS loc_id,
                          l.name                AS loc_name,
                          p.id                  AS photo_id,
                          p.alt_text            AS photo_alt_text,
                          p.url                 AS photo_url,
                          r.avg_rating          AS avg_rating
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating
                                       FROM rating
                                       GROUP BY id_location) r ON l.id = r.id_location
                   WHERE l.status = 'approved'
                   ORDER BY avg_rating DESC 
                    LIMIT 1
                   """)
    #Zpracuje pouze první výskyt
    row = cursor.fetchone()

    location = {
        "id": row[0],
        "name": row[1],
        "photo": None,
        "avg_rating": row[5]
    }

    # Pokud sloupce s fotkou nejsou None
    if row[2] is not None:
        location["photo"] = {
            "id": row[2],
            "alt_text": row[3],
            "url": row[4]
        }
    return location

def get_newest_location(conn: sqlite3.Connection) -> Dict[str, Any]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.id         AS loc_id,
                          l.name       AS loc_name,
                          p.id         AS photo_id,
                          p.alt_text   AS photo_alt_text,
                          p.url        AS photo_url
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                    WHERE l.status = 'approved'
                   ORDER BY l.id DESC
                   LIMIT 1
                   """)
    # Zpracuje pouze první výskyt
    row = cursor.fetchone()

    location = {
        "id": row[0],
        "name": row[1],
        "photo": None,
    }

    # Pokud sloupce s fotkou nejsou None
    if row[2] is not None:
        location["photo"] = {
            "id": row[2],
            "alt_text": row[3],
            "url": row[4]
        }
    return location

def list_locations_by_avg_rating(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("""
                        SELECT l.id                  AS loc_id,
                        l.name                AS loc_name,
                        l.description AS loc_description,
                        p.id                  AS photo_id,
                        p.alt_text            AS photo_alt_text,
                        p.url                 AS photo_url,
                        r.avg_rating          AS avg_rating
                        FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating
                                       FROM rating
                                       GROUP BY id_location) r ON l.id = r.id_location
                        WHERE l.status = 'approved'
                        GROUP BY l.id
                   ORDER BY avg_rating DESC
                   """)
    locations = []

    for row in cursor.fetchall():
        loc_data = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "photo": None
        }

        if row[3] is not None:
            loc_data["photo"] = {
                "id": row[3],
                "alt_text": row[4],
                "url": row[5]
            }

        locations.append(loc_data)

    return locations

def list_locations_by_newest(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.id          AS loc_id,
                          l.name        AS loc_name,
                          l.description AS loc_description,
                          p.id          AS photo_id,
                          p.alt_text    AS photo_alt_text,
                          p.url         AS photo_url,
                          r.avg_rating  AS avg_rating
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating
                                       FROM rating
                                       GROUP BY id_location) r ON l.id = r.id_location
                    WHERE l.status = 'approved'
                    GROUP BY l.id
                   ORDER BY l.id DESC
                   """)
    locations = []

    for row in cursor.fetchall():
        loc_data = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "photo": None
        }

        if row[3] is not None:
            loc_data["photo"] = {
                "id": row[3],
                "alt_text": row[4],
                "url": row[5]
            }

        locations.append(loc_data)

    return locations

def list_locations_by_most_comments(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.id          AS loc_id,
                          l.name        AS loc_name,
                          l.description AS loc_description,
                          p.id          AS photo_id,
                          p.alt_text    AS photo_alt_text,
                          p.url         AS photo_url,
                          r.avg_rating  AS avg_rating
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating FROM rating GROUP BY id_location) r ON l.id = r.id_location
                            LEFT JOIN (SELECT id_location, COUNT(id) AS com_count FROM comment GROUP BY id_location) c ON l.id = c.id_location
                    WHERE l.status = 'approved'
                GROUP BY l.id
                ORDER BY com_count DESC
                   """)
    locations = []

    for row in cursor.fetchall():
        loc_data = {
            "id": row[0],
            "name": row[1],
            "photo": None
        }

        if row[2] is not None:
            loc_data["photo"] = {
                "id": row[2],
                "alt_text": row[3],
                "url": row[4]
            }

        locations.append(loc_data)

def list_locations_added_by_concrete_user(conn: sqlite3.Connection, id_user:int) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("""
                SELECT
                          l.name        AS loc_name,
                          p.alt_text    AS photo_alt_text,
                          p.url         AS photo_url
                FROM location l
                    LEFT JOIN photo p ON l.id = p.id_location
                WHERE l.status = 'approved' AND  l.id_user = :id_user
                GROUP BY l.id
                ORDER BY l.id DESC
                   """, {"id_user": id_user})
    locations = []
    for row in cursor.fetchall():
        loc_data = {
            "name": row[0],
            "photo": None
        }
        if row[1] is not None:
            loc_data["photo"] = {
                "alt_text": row[1],
                "url": row[2]
            }
        locations.append(loc_data)

    return locations