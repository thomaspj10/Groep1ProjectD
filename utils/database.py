import sqlite3
from hashlib import sha256

# create one connection to the sqlite database
# a database will be created if it does not yet exists
# get a connection by importing this file and calling the get_connection function
def get_connection() -> sqlite3.Connection:
    return sqlite3.connect("./db.sqlite")

def setup():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS user( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        telephone TEXT,
        authentication_level INTEGER,
        receive_notifications INTEGER
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS event(
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_id INTEGER,
        time INTEGER,
        latitude FLOAT,
        longitude FLOAT,
        sound_type TEXT,
        probability INTEGER,
        sound TEXT,
        pdf BLOB
    )""")

    password = sha256(("admin1MPlGCnOwSywPTg5BXbZ").encode("utf-8")).hexdigest()

    cursor.execute(f"""INSERT INTO user (username, password, email, telephone, authentication_level, receive_notifications) 
        VALUES ('Admin', '{password}', 'admin@alten.nl', '0612345678', 2, False)
    """)

    connection.commit()