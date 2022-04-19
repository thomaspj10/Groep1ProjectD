import sqlite3
from sqlite3 import Error

# creates a connection to the sqlite database specified in the db_file
# a database will be created if the database does not yet exists
# create a connection by importing this file and calling the create_connection function
def create_connection():
    db_file = "./application/db.sqlite"
    return sqlite3.connect(db_file)



# Database consists of the following tables:

# create table if not exists user(              
#   id integer primary key autoincrement,
#   username text not null,
#   password text not null,
#   email text,
#   telephone text,
#   authentication_level integer)

# create table if not exists node(
#   node_id integer primary key autoincrement,
#   time text,
#   latitude float,
#   longitude float,
#   sound_type,
#   probability integer,
#   sound text)