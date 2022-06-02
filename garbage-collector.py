import time
from utils import database, logger

def run():
  curr_unix_time = round(time.time())
  unix_1_week = 604800
  
  con = database.get_connection()
  cur = con.cursor()
  
  cur.execute(f"""
    SELECT COUNT(*)
    FROM event
    WHERE time BETWEEN {curr_unix_time - unix_1_week} AND {curr_unix_time}
  """)
  
  count = cur.fetchone()
  
  cur.execute(f"""
    UPDATE event
    SET pdf=NULL
    WHERE time BETWEEN {curr_unix_time - unix_1_week} AND {curr_unix_time}
  """)
  con.commit()
  