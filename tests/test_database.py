import sqlite3
import unittest
import utils.database as database

class TestDatabase(unittest.TestCase):

    def test_database_connection(self):
        self.assertNotEqual(database.get_connection(), None)
        self.assertIsInstance(database.get_connection(), sqlite3.Connection)
        
    def test_tables_existence(self):
        conn = database.get_connection()
        cursor = conn.cursor()
        
        self.assertNotEqual(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='event';").fetchone(), None, "The table 'event' does not exist.")
        self.assertNotEqual(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';").fetchone(), None, "The table 'user' does not exist.")