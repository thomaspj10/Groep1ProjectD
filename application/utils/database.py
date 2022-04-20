import sqlite3

# create one connection to the sqlite database
# a database will be created if it does not yet exists
# get a connection by importing this file and calling the get_connection function
def get_connection():
    return sqlite3.connect("./db.sqlite") 

def insert_into_event_table(connection, data) -> int:
    """
    Insert data which hold the data of a node event
    :param conn: the Connection object
    :param data:
    :return 0 or -1:
    """
    if len(data) != 7:
        raise TypeError(f"Query data collection has to be of length 7, currenlty: {len(data)}")
        
    try:
        query = ''' INSERT INTO event (node_id, time, latitude, longitude, sound_type, probability, sound) VALUES (?,?,?,?,?,?,?) '''
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        return 0
    
    except TypeError as err:
        print('Handling run-time error:', err)
        return -1
        
def select_user_by_receive_notifications(connection, receive_notifications: bool) -> list:
    """
    Query users by receive_notifications
    :param conn: the Connection object
    :param receive_notifications:
    :return a list of users:
    """
    
    cursor = connection.cursor()
    
    # If receive_notifications true add NOT to to query, else nothing
    cursor.execute(f"SELECT * FROM user WHERE {'NOT ' if receive_notifications == True else ''}receive_notifications")
    return cursor.fetchall()

# Database consists of the following tables:

# create table if not exists user(              
#   id integer primary key autoincrement,
#   username text not null,
#   password text not null,
#   email text,
#   telephone text,
#   authentication_level integer,
#   receive_notifications boolean)

# create table if not exists event(
#   node_id integer primary key autoincrement,
#   time text,
#   latitude float,
#   longitude float,
#   sound_type,
#   probability integer,
#   sound text)