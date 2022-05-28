from datetime import datetime
import utils.database as database
from random import randint, uniform
import time as ti

def __run() -> None:
    database.setup()
    unix_5_min = 300
    unix_1_d = 86400
    unix_8_d = unix_1_d * 8
    
    print("# Setting up #")
    
    # 5 recent events
    print("Settings up 5 recent events ...")
    for i in range(0, 5):
        time = uniform(ti.time() - unix_5_min, ti.time())
        time = round(time)
        
        event = __generate_data(time)
        __insert_into_database(event)
    
    # 100 older events
    print("Settings up 100 older events ...")
    for i in range(0, 100):
        time = uniform(ti.time() - unix_8_d, ti.time())
        time = round(time)
    
        event = __generate_data(time)
        __insert_into_database(event)
        
        
    print("# Setup done #")
    print("# Starting mock mqtt-broker #")
    # new recents events every 30-60 seconds
    while True:
        ti.sleep(uniform(30, 60))
        print(f"New event: {datetime.now()}")
        time = round(ti.time())
        event = __generate_data(time)
        __insert_into_database(event)
        

def __generate_data(event_time) -> dict:
    sound_types = ["unknown", "gunshot", "vehicle", "animal"]
    
    node_id = randint(1,30)
    time = event_time
    latitude = uniform(-0.759751, -2.977670)
    longitude = uniform(18.624196, 23.065636)
    probability = randint(0,100)
    sound_type = sound_types[randint(0, len(sound_types)-1)]
    sound = "http://95.217.2.100:8000/55020-4-0-0.wav"
    
    event = {
        "node_id": node_id,
        "time": time,
        "latitude": latitude,
        "longitude": longitude,
        "probability": probability,
        "sound_type": sound_type,
        "sound": sound
    }
    return event
    
def __insert_into_database(event: dict) -> None:
    con = database.get_connection()
    con.execute(f"""
                INSERT INTO event (node_id, time, latitude, longitude, probability, sound_type, sound) 
                VALUES ({event["node_id"]}, {event["time"]}, {event["latitude"]}, {event["longitude"]}, {event["probability"]}, '{event["sound_type"]}', '{event["sound"]}');
                """)
    con.commit()
    
    # print(event)
    
    
if __name__ == "__main__":
    __run()