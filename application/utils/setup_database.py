from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""create table if not exists user( 
    id integer primary key autoincrement,
    username text not null,
    password text not null,
    email text,
    telephone text,
    authentication_level integer,
    receive_notifications integer
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

cursor.execute("""INSERT INTO user (username, password, email, telephone, authentication_level, receive_notifications) 
    VALUES ('Admin', 'admin', 'admin@alten.nl', '0612345678', 2, 1)
""")

connection.commit()
