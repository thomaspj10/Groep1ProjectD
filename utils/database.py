import sqlite3

# create one connection to the sqlite database
# a database will be created if it does not yet exists
# get a connection by importing this file and calling the get_connection function
def get_connection():
    return sqlite3.connect("./db.sqlite")
def insert_into_event_table(connection, data) -> tuple[int, int]:
    """
    Insert data which hold the data of a node event
    :param conn: the Connection object
    :param data:
    :return 0 or -1:
    """
    if len(data) != 7:
        raise TypeError(f"Query data collection has to be of length 7, currently: {len(data)}")
        
    try:
        query = ''' INSERT INTO event (node_id, time, latitude, longitude, sound_type, probability, sound) VALUES (?,?,?,?,?,?,?) '''
        cursor = connection.cursor()
        cursor.execute(query, data)
        
        # Get the event id
        cursor.execute(f"SELECT last_insert_rowid()")
        event_id, = cursor.fetchone()
        
        connection.commit()
        return 0, event_id
    
    except TypeError as err:
        print('Handling run-time error:', err)
        return -1, 0
        
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