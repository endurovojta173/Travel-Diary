from database.database import open_connection

DDL = """
CREATE TABLE role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    password_hash VARCHAR NOT NULL,
    id_role INTEGER,
    FOREIGN KEY (id_role) REFERENCES role(id)
);

CREATE TABLE location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    description VARCHAR,
    date_location_added TEXT NOT NULL,
    status VARCHAR NOT NULL,
    id_user INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES user(id)
);

CREATE TABLE photo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    alt_text VARCHAR,
    url VARCHAR NOT NULL,
    id_location INTEGER NOT NULL,
    FOREIGN KEY (id_location) REFERENCES location(id)
);
    
CREATE TABLE favorite_location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    id_location INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES user(id),
    FOREIGN KEY (id_location) REFERENCES location(id),
    UNIQUE(id_user, id_location)
);
    
CREATE TABLE comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text VARCHAR NOT NULL,
    id_user INTEGER NOT NULL,
    id_location INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES user(id),
    FOREIGN KEY (id_location) REFERENCES location(id)
);
    
CREATE TABLE rating (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    id_user INTEGER NOT NULL,
    id_location INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES user(id),
    FOREIGN KEY (id_location) REFERENCES location(id),
    UNIQUE(id_user, id_location)  -- Jeden uživatel může hodnotit lokaci jen jednou
);
"""

if __name__ == "__main__":
    with open_connection() as c:
        c.executescript(DDL)
        c.commit()
        print("DB initialized.")

