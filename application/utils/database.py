import sqlite3

# create one connection to the sqlite database
# a database will be created if it does not yet exists
# get a connection by importing this file and calling the get_connection function
def get_connection():
    return sqlite3.connect("./db.sqlite")

def insert_into_event_table(connection, data):
    if data.length != 7:
        raise TypeError(f"Query data collection has to be of length 7, currenlty: {data.length}")
        
    try:
        query = ''' INSERT INTO event (node_id, time, latitude, longitude, sound_type, probability, sound) VALUES (?,?,?,?,?,?,?) '''
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
    
    except TypeError as err:
        print('Handling run-time error:', err)
        


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
#   event_id integer primary key autoincrement,
#   node_id integer,
#   time text,
#   latitude float,
#   longitude float,
#   sound_type,
#   probability integer,
#   sound text)