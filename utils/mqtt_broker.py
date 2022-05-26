import datetime
import json
import pandas as pd
from paho.mqtt import client as mqtt_client
from utils import notifications, database, settings
from uuid import uuid4

__settings = settings.read_settings()

__HOST = __settings["mqtt_broker"]["ipv4"]
__PORT = __settings["mqtt_broker"]["port"]
__TOPIC = __settings["mqtt_broker"]["topic"]
__USERNAME = __settings["mqtt_broker"]["username"]
__PASSWORD = __settings["mqtt_broker"]["password"]
__CLIENTID = __settings["mqtt_broker"]["client_id"]

def connect() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker.")
        else:
            print("Failed to connect, return code %d\n" % rc)

    client = mqtt_client.Client(__CLIENTID)
    client.username_pw_set(__USERNAME, __PASSWORD)
    client.on_connect = on_connect
    client.connect(__HOST, __PORT)
    return client


def subscribe(client: mqtt_client) -> None:
    def on_message(client, userdata, msg):
        payload_jsonstring = msg.payload.decode()
        payload = json.loads(payload_jsonstring)
        
        try: 
            query_data = [
                payload["nodeId"], payload["time"],
                payload["latitude"], payload["longitude"],
                payload["sound_type"], payload["probability"],
                payload["sound"]
            ]
            
            
            db_conn = database.get_connection()
        
            if len(query_data) != 7:
                raise TypeError(f"Query data collection has to be of length 7, currently: {len(query_data)}")
                
            succes: bool = False
            try:
                query = ''' INSERT INTO event (node_id, time, latitude, longitude, sound_type, probability, sound) VALUES (?,?,?,?,?,?,?) '''
                cursor = db_conn.cursor()
                cursor.execute(query, query_data)
                db_conn.commit()
                succes = True
            
            except TypeError as err:
                print('Handling run-time error:', err)
                succes = False
                
            
            if succes:
                print("Succeeded to insert data into database.")
                
                users = pd.read_sql("SELECT * FROM user WHERE receive_notifications == 1", db_conn)
                for index, user in users.iterrows():
                    try:
                        time = datetime.datetime.fromtimestamp(int(payload['time']))
                        msg = f"\n{time}\n An event occured at node {payload['nodeId']}.\n Latitude: {payload['latitude']}, Longitude: {payload['longitude']}.\n {payload['probability']}% probability of a {payload['sound_type']}."
                        notifications.send_notification(user["telephone"], msg)
                
                    except Exception as err:
                        print('Handling run-time error:', err)
            
            else:
                print("Failed to insert data into database.")
            
        except Exception as err:
            print('Handling run-time error:', err)
        
    client.subscribe(__TOPIC)
    client.on_message = on_message
