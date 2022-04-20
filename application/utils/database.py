import sqlite3

# create one connection to the sqlite database
# a database will be created if it does not yet exists
# get a connection by importing this file and calling the get_connection function
def get_connection():
    return sqlite3.connect("./application/db.sqlite")


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