from database import get_connection
from hashlib import sha256

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
    sound TEXT
)""")

password = sha256(("admin1MPlGCnOwSywPTg5BXbZ").encode("utf-8")).hexdigest()

cursor.execute(f"""INSERT INTO user (username, password, email, telephone, authentication_level, receive_notifications) 
    VALUES ('Admin', '{password}', 'admin@alten.nl', '0612345678', 2, False)
""")

connection.commit()