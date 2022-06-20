import time
from utils import database, logger

def run():
  curr_unix_time = round(time.time())
  unix_1_week = 604800
  
  try:
    con = database.get_connection()
    cur = con.cursor()
    
    cur.execute(f"""
      SELECT COUNT(*)
      FROM event
      WHERE pdf IS NOT NULL AND time BETWEEN {curr_unix_time - unix_1_week} AND {curr_unix_time}
    """)
    
    count = cur.fetchall()[0][0]
    
    cur.execute(f"""
      UPDATE event
      SET pdf=NULL
      WHERE time BETWEEN {curr_unix_time - unix_1_week} AND {curr_unix_time}
    """)
    con.commit()
    
    info = f"Removed {count} old pdf files from database"
    
  except Exception as err:
    info = f"Handling run-time error: {err}"

  print(f"[-] {info}")
  # logger.info(
  #   activity="Garbage collector",
  #   information=info
  # )
  
def main():
  while True:
    run()
    time.sleep(3600)
  
if __name__ == "__main__":
  main()