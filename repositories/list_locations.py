from typing import List, Dict, Any, Optional
import sqlite3

def list_locations_with_photos_and_rating(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.id          AS loc_id,
                          l.name        AS loc_name,
                          l.description AS loc_description,
                          l.id_status      AS loc_status,
                          p.id          AS photo_id,
                          p.alt_text    AS photo_alt_text,
                          p.url         AS photo_url,
                          r.avg_rating  AS avg_rating
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating
                                       FROM rating
                                       GROUP BY id_location) r ON l.id = r.id_location
                   WHERE l.id_status = 1
                   ORDER BY l.id
                   """)

    locations: Dict[int, Dict[str, Any]] = {}

    for row in cursor.fetchall():
        loc_id = row[0]

        if loc_id not in locations:
            locations[loc_id] = {
                "id": loc_id,
                "name": row[1],
                "description": row[2],
                "photos": [],
                "avg_rating": row[7]
            }

        if row[4] is not None:
            locations[loc_id]["photos"].append({
                "id": row[4],
                "alt_text": row[5],
                "url": row[6]
            })

    return list(locations.values())


def get_location_by_id_with_photos_and_rating(conn: sqlite3.Connection, location_id: int) -> Dict[str, Any]:
    cursor = conn.cursor()
    # SQL
    cursor.execute("""
                   SELECT l.id                  AS loc_id,
                          l.name                AS loc_name,
                          l.description         AS loc_description,
                          l.date_location_added AS loc_date_location_added,
                          p.id                  AS photo_id,
                          p.alt_text            AS photo_alt_text,
                          p.url                 AS photo_url,
                          r.avg_rating          AS avg_rating
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating
                                       FROM rating
                                       GROUP BY id_location) r ON l.id = r.id_location
                   WHERE l.id = :id
                     AND l.id_status = 1
                   ORDER BY l.id
                   """, {"id": location_id})

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

        if row[4] is not None:
            location["photos"].append({
                "id": row[4],
                "alt_text": row[5],
                "url": row[6]
            })

    return location


def get_five_random_locations(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    # Vybere 5 random lokací
    cursor.execute("""
                   SELECT l.id       AS loc_id,
                          l.name     AS loc_name,
                          p.id       AS photo_id,
                          p.alt_text AS photo_alt_text,
                          p.url      AS photo_url
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                   WHERE l.id_status = 1
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
                   SELECT l.id         AS loc_id,
                          l.name       AS loc_name,
                          p.id         AS photo_id,
                          p.alt_text   AS photo_alt_text,
                          p.url        AS photo_url,
                          r.avg_rating AS avg_rating
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating
                                       FROM rating
                                       GROUP BY id_location) r ON l.id = r.id_location
                   WHERE l.id_status = 1
                   ORDER BY avg_rating DESC
                   LIMIT 1
                   """)
    # Zpracuje pouze první výskyt
    row = cursor.fetchone()
    if row is None:
        return None

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
                   SELECT l.id       AS loc_id,
                          l.name     AS loc_name,
                          p.id       AS photo_id,
                          p.alt_text AS photo_alt_text,
                          p.url      AS photo_url
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                   WHERE l.id_status = 1
                   ORDER BY l.id DESC
                   LIMIT 1
                   """)
    # Zpracuje pouze první výskyt
    row = cursor.fetchone()

    if row is None:
        return None

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
                   WHERE l.id_status = 1
                   GROUP BY l.id
                   ORDER BY avg_rating DESC
                   """)
    locations = []

    for row in cursor.fetchall():
        loc_data = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "photo": None,
            "avg_rating": row[6]
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
                   WHERE l.id_status = 1
                   GROUP BY l.id
                   ORDER BY l.id DESC
                   """)
    locations = []

    for row in cursor.fetchall():
        loc_data = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "photo": None,
            "avg_rating": row[6]
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
                   SELECT l.id,
                          l.name,
                          l.description,
                          p.id,
                          p.alt_text,
                          p.url,
                          r.avg_rating
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating FROM rating GROUP BY id_location) r
                                      ON l.id = r.id_location
                            LEFT JOIN (SELECT id_location, COUNT(id) AS com_count FROM comment GROUP BY id_location) c
                                      ON l.id = c.id_location
                   WHERE l.id_status = 1
                   GROUP BY l.id
                   ORDER BY com_count DESC
                   """)
    locations = []

    for row in cursor.fetchall():
        loc_data = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "photo": None,
            "avg_rating": row[6]
        }

        if row[3] is not None:
            loc_data["photo"] = {
                "id": row[3],
                "alt_text": row[4],
                "url": row[5]
            }
        locations.append(loc_data)

    return locations


def list_locations_added_by_concrete_user(conn: sqlite3.Connection, id_user: int) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.id,
                          l.name,
                          l.description,
                          p.alt_text,
                          p.url,
                          (SELECT AVG(rating) FROM rating WHERE id_location = l.id)
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                   WHERE l.id_status = 1
                     AND l.id_user = :id_user
                   GROUP BY l.id
                   ORDER BY l.id DESC
                   """, {"id_user": id_user})
    locations = []
    for row in cursor.fetchall():
        rating = row[5] if row[5] is not None else 0

        loc_data = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "photo": None,
            "avg_rating": rating
        }

        if row[3] is not None:
            loc_data["photo"] = {
                "alt_text": row[3],
                "url": row[4]
            }
        locations.append(loc_data)

    return locations


def add_location_to_favorites(conn: sqlite3.Connection, id_user: int, id_location: int) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       INSERT INTO favorite_location(id_user, id_location)
                       VALUES (?, ?)
                       """, (id_user, id_location))

        new_location_id = cursor.lastrowid
        conn.commit()
        return new_location_id
    except:
        print("Error adding location to favorites")
        conn.rollback()  # Vrátíme změny
        return None


def add_location_to_visited(conn: sqlite3.Connection, id_user: int, id_location: int) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       INSERT INTO visited_location(id_user, id_location)
                       VALUES (?, ?)
                       """, (id_user, id_location))

        new_location_id = cursor.lastrowid
        conn.commit()
        return new_location_id
    except:
        print("Error adding location to favorites")
        conn.rollback()  # Vrátíme změny
        return None


def remove_location_from_favorite(conn: sqlite3.Connection, id_user: int, id_location: int) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       DELETE
                       FROM favorite_location
                       WHERE id_user = ?
                         AND id_location = ?
                       """, (id_user, id_location))
        conn.commit()
        return True
    except:
        print("Error removing location from favorites")
        conn.rollback()


def remove_location_from_visited(conn: sqlite3.Connection, id_user: int, id_location: int) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       DELETE
                       FROM visited_location
                       WHERE id_user = ?
                         AND id_location = ?
                       """, (id_user, id_location))
        conn.commit()
        return True
    except:
        print("Error removing location from visited")
        conn.rollback()


def is_location_favorite(conn: sqlite3.Connection, user_id: int, location_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT 1
                   FROM favorite_location
                   WHERE id_user = ?
                     AND id_location = ?
                   """, (user_id, location_id))
    return cursor.fetchone() is not None


def is_location_visited(conn: sqlite3.Connection, user_id: int, location_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT 1
                   FROM visited_location
                   WHERE id_user = ?
                     AND id_location = ?
                   """, (user_id, location_id))

    return cursor.fetchone() is not None


def list_my_visited_locations(conn: sqlite3.Connection, user_id: int) -> List[Dict[str, str]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.id,
                          l.name,
                          l.description,
                          p.alt_text,
                          p.url,
                          (SELECT AVG(rating) FROM rating WHERE id_location = l.id)
                   FROM visited_location v
                            JOIN location l ON v.id_location = l.id
                            LEFT JOIN photo p ON l.id = p.id_location
                   WHERE v.id_user = :user_id
                   GROUP BY l.id
                   ORDER BY l.id DESC
                   """, (user_id,))

    locations = []
    for row in cursor.fetchall():
        rating = row[5] if row[5] is not None else 0

        loc_data = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "photo": None,
            "avg_rating": rating
        }

        if row[4] is not None:
            loc_data["photo"] = {
                "alt_text": row[3],
                "url": row[4]
            }

        locations.append(loc_data)

    return locations


def list_my_favorite_locations(conn: sqlite3.Connection, user_id: int) -> List[Dict[str, str]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.id,
                          l.name,
                          l.description,
                          p.alt_text,
                          p.url,
                          (SELECT AVG(rating) FROM rating WHERE id_location = l.id)
                   FROM favorite_location f
                            JOIN location l ON f.id_location = l.id
                            LEFT JOIN photo p ON l.id = p.id_location
                   WHERE f.id_user = :user_id
                   GROUP BY l.id
                   ORDER BY l.id DESC
                   """, {"user_id": user_id})

    locations = []
    for row in cursor.fetchall():
        rating = row[5] if row[5] is not None else 0

        loc_data = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "photo": None,
            "avg_rating": rating
        }

        if row[4] is not None:
            loc_data["photo"] = {
                "alt_text": row[3],
                "url": row[4]
            }

        locations.append(loc_data)

    return locations


def list_my_locations_with_pending_status(conn: sqlite3.Connection, user_id: int) -> List[Dict[str, str]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.id,
                          l.name,
                          l.description,
                          p.alt_text,
                          p.url,
                          (SELECT AVG(rating) FROM rating WHERE id_location = l.id)
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                   WHERE l.id_user = :user_id
                     AND l.id_status = 2
                   GROUP BY l.id
                   ORDER BY l.id DESC
                   """, (user_id,))

    locations = []
    for row in cursor.fetchall():
        rating = row[5] if row[5] is not None else 0

        loc_data = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "photo": None,
            "avg_rating": rating
        }

        if row[4] is not None:
            loc_data["photo"] = {
                "alt_text": row[3],
                "url": row[4]
            }
        locations.append(loc_data)

    return locations


def list_pending_locations(conn: sqlite3.Connection) -> List[Dict[str, str]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.id,
                          l.name,
                          p.url,
                          p.alt_text,
                          u.name AS author_name
                   FROM location l
                            JOIN user u ON l.id_user = u.id
                            LEFT JOIN photo p ON l.id = p.id_location
                   WHERE l.id_status = 2
                   GROUP BY l.id
                   """)

    locations = []
    for row in cursor.fetchall():
        loc_data = {
            "id": row[0],
            "name": row[1],
            "photo": None,
            "author": row[4]  # Jméno autora
        }

        if row[2] is not None:
            loc_data["photo"] = {
                "url": row[2],
                "alt_text": row[3]
            }

        locations.append(loc_data)

    return locations


def get_pending_location_detail(conn: sqlite3.Connection, location_id: int) -> Dict[str, Any]:
    cursor = conn.cursor()
    # SQL
    cursor.execute("""
                   SELECT l.id                  AS loc_id,
                          l.name                AS loc_name,
                          l.description         AS loc_description,
                          l.date_location_added AS loc_date_location_added,
                          p.id                  AS photo_id,
                          p.alt_text            AS photo_alt_text,
                          p.url                 AS photo_url,
                          r.avg_rating          AS avg_rating
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating
                                       FROM rating
                                       GROUP BY id_location) r ON l.id = r.id_location
                   WHERE l.id = :id
                     AND l.id_status = 2
                   ORDER BY l.id
                   """, {"id": location_id})

    # Inicializace slovníku
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


def search_locations(conn: sqlite3.Connection, query: str) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    like_query = f"%{query}%"

    # 2. Pro počítání výskytů potřebujeme čisté slovo malé: "hrad"
    # (SQLite funkce REPLACE je case-sensitive, proto musíme vše převést na LOWER)
    clean_query = query.lower()

    cursor.execute("""
                   SELECT l.id,
                          l.name,
                          l.description,
                          p.url,
                          p.alt_text,
                          r.avg_rating,

                          --VÝPOČET RELEVANCE (SKÓRE)
                          (
                              --Skóre v názvu: (Původní délka - Délka po odstranění slova)
                              (LENGTH(LOWER(l.name)) - LENGTH(REPLACE(LOWER(l.name), ?, '')))
                                  +
                                  --Skóre v popisu (ošetřeno IFNULL, kdyby popis chyběl)
                              (LENGTH(LOWER(IFNULL(l.description, ''))) -
                               LENGTH(REPLACE(LOWER(IFNULL(l.description, '')), ?, '')))
                              ) AS relevance_score

                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                            LEFT JOIN (SELECT id_location, AVG(rating) AS avg_rating FROM rating GROUP BY id_location) r
                                      ON l.id = r.id_location

                   WHERE l.id_status = 1
                     AND (l.name LIKE ? OR l.description LIKE ?)

                   GROUP BY l.id

                   -- Řadíme podle skóre od nejvyššího
                   ORDER BY relevance_score DESC
                   """, (clean_query, clean_query, like_query, like_query))

    locations = []
    for row in cursor.fetchall():
        loc_data = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "avg_rating": round(row[5], 1) if row[5] else 0,
            "photo": None
        }
        if row[3] is not None:
            loc_data["photo"] = {"url": row[3], "alt_text": row[4]}

        locations.append(loc_data)

    return locations


def get_location_with_photos_pending_or_approved_status(conn: sqlite3.Connection, location_id: int) -> Dict[str, Any]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.id                  AS loc_id,
                          l.name                AS loc_name,
                          l.description         AS loc_description,
                          l.date_location_added AS loc_date_location_added,
                          l.id_status           AS loc_status_id, -- Přidal jsem i ID statusu, může se hodit
                          p.id                  AS photo_id,
                          p.alt_text            AS photo_alt_text,
                          p.url                 AS photo_url
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                   WHERE l.id = :id
                     AND l.id_status IN (1, 2)
                   ORDER BY l.id
                   """, {"id": location_id})

    location = {}

    for row in cursor.fetchall():
        location = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "date_location_added": row[3],
            "photos": [],
        }

        if row[4] is not None:
            location["photos"].append({
                "id": row[4],
                "alt_text": row[5],
                "url": row[6]
            })

    return location

def get_location_status(conn: sqlite3.Connection, location_id: int) -> int:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT id_status
                       FROM location
                       WHERE id = ?
                       """, (location_id,))
        return cursor.fetchone()[0]