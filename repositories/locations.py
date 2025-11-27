from typing import List, Dict, Any, Optional
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
                     AND l.status = 'approved'
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
                   WHERE l.status = 'approved'
                   ORDER BY avg_rating DESC
                   LIMIT 1
                   """)
    # Zpracuje pouze první výskyt
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
                   SELECT l.id       AS loc_id,
                          l.name     AS loc_name,
                          p.id       AS photo_id,
                          p.alt_text AS photo_alt_text,
                          p.url      AS photo_url
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
                   WHERE l.status = 'approved'
                   GROUP BY l.id
                   ORDER BY com_count DESC
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

def list_locations_added_by_concrete_user(conn: sqlite3.Connection, id_user: int) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.id       AS loc_id,
                          l.name     AS loc_name,
                          p.alt_text AS photo_alt_text,
                          p.url      AS photo_url
                   FROM location l
                            LEFT JOIN photo p ON l.id = p.id_location
                   WHERE l.status = 'approved'
                     AND l.id_user = :id_user
                   GROUP BY l.id
                   ORDER BY l.id DESC
                   """, {"id_user": id_user})
    locations = []
    for row in cursor.fetchall():
        loc_data = {
            "id": row[0],
            "name": row[1],
            "photo": None
        }
        if row[2] is not None:
            loc_data["photo"] = {
                "alt_text": row[2],
                "url": row[3]
            }
        locations.append(loc_data)

    return locations


def add_new_location(conn: sqlite3.Connection, id_user: int, name: str, description: str, photos: Optional[List[Dict[str, str]]] = None) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       INSERT INTO location(name, description, id_user, status)
                       VALUES (?, ?, ?, 'pending')
                       """, (name, description, id_user))

        new_location_id = cursor.lastrowid
        conn.commit()
        return new_location_id
    except:
        print("Error adding new location")
        conn.rollback()  #Vrátíme změny
        return None

def add_location_to_favorites(conn: sqlite3.Connection, id_user: int, id_location: int) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO favorite_location(id_user, id_location)
                VALUES (?,?)
        """,(id_user, id_location))

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
                VALUES (?,?)
        """,(id_user, id_location))

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
            DELETE FROM favorite_location WHERE id_user = ? AND id_location = ?
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
        DELETE FROM visited_location WHERE id_user = ? AND id_location = ?
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

def list_comments(conn:sqlite3.Connection, id_location: int) -> List[Dict[str, str]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT   c.id,   
                            u.name,
                            c.comment_time,
                            c.text
                   FROM comment c
                            JOIN user u ON c.id_user = u.id
                   WHERE c.id_location = ?
                   ORDER BY c.id DESC
                   """, (id_location,))

    comments = []
    for row in cursor.fetchall():
        comments.append({
            "comment_id": row[0],
            "author": row[1],
            "date": row[2],
            "text": row[3],
        })

    return comments

def add_comment_to_location(conn: sqlite3.Connection, id_user: int, id_location: int, comment_text: str) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO comment(id_user, id_location, text)
            VALUES (?, ?, ?)
                       """, (id_user, id_location, comment_text))
        conn.commit()
    except:
        print("Error adding comment to location")
        conn.rollback()

def remove_my_comment_from_location(conn: sqlite3.Connection, id_user: int, id_location: int) -> Optional[int]:
    cursor = conn.cursor()
    try:
        cursor.execute("""
        DELETE FROM comment WHERE id_user = ? AND id_location = ?
                       """,(id_user, id_location))
        conn.commit()
    except:
        print("Error removing comment from location")
        conn.rollback()

def list_my_visited_locations(conn:sqlite3.Connection, user_id: int) -> List[Dict[str, str]]:
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT l.id,
                          l.name,
                          p.url ,
                          p.alt_text
                   FROM visited_location v
                            JOIN location l ON v.id_location = l.id
                            LEFT JOIN photo p ON l.id = p.id_location
                   WHERE v.id_user = :user_id
                   GROUP BY l.id
                   """, (user_id,))

    locations = []
    for row in cursor.fetchall():
        loc_data = {
            "id": row[0],
            "name": row[1],
            "photo": None
        }
        if row[2] is not None:
            loc_data["photo"] = {
                "url": row[2],
                "alt_text": row[3]
            }

        locations.append(loc_data)

    return locations

def list_my_favorite_locations(conn: sqlite3.Connection, user_id: int) -> List[Dict[str, str]]:
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT l.id,
                          l.name,
                          p.url ,
                          p.alt_text
                    FROM favorite_location f
                            JOIN location l ON f.id_location = l.id
                            LEFT JOIN photo p ON l.id = p.id_location
                    WHERE f.id_user = :user_id
                    GROUP BY l.id
                   """,(user_id,))

    locations = []
    for row in cursor.fetchall():
        loc_data = {
            "id": row[0],
            "name": row[1],
            "photo": None
        }
        if row[2] is not None:
            loc_data["photo"] = {
                "url": row[2],
                "alt_text": row[3]
            }

        locations.append(loc_data)

    return locations