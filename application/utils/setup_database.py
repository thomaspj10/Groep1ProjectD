from database import get_connection
from hashlib import sha256

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""create table if not exists user( 
    id integer primary key autoincrement,
    username text not null,
    password text not null,
    email text,
    telephone text,
    authentication_level integer,
    receive_notifications boolean
)""")

cursor.execute("""create table if not exists event(
    event_id integer primary key autoincrement,
    node_id integer,
    time integer,
    latitude float,
    longitude float,
    sound_type text,
    probability integer,
    sound text
)""")

password = sha256(("admin1MPlGCnOwSywPTg5BXbZ").encode("utf-8")).hexdigest()

cursor.execute(f"""INSERT INTO user (username, password, email, telephone, authentication_level, receive_notifications) 
    VALUES ('Admin', '{password}', 'admin@alten.nl', '0612345678', 2, False)
""")

connection.commit()