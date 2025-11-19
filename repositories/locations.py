from typing import List, Dict, Any, Optional
import sqlite3

def list_locations(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    rows = conn.execute('SELECT * FROM Location').fetchall()
    return [dict(r) for r in rows]