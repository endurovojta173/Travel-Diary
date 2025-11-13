from database.database import open_connection

DDL = """
CREATE TABLE IF NOT EXISTS items(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  price REAL NOT NULL
);
"""

if __name__ == "__main__":
    with open_connection() as c:
        c.executescript(DDL)
        c.commit()
        print("DB initialized.")
