from paho.mqtt import client as mqtt_client
import json
import pandas as pd
import utils.notifications as notify
from utils.database import insert_into_event_table, select_user_by_receive_notifications
from uuid import uuid4

BROKER = "95.217.2.100"
PORT = 1883
TOPIC = "chengeta/notifications"
USERNAME = "chengeta_user"
PASSWORD = "chengeta2022"

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker.")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(str(uuid4()))
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


def subscribe(client: mqtt_client, db_connection) -> None:
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
            
            succes = insert_into_event_table(db_connection, query_data) == 0
            if succes:
                print("Succeeded to insert data into database.")
                users = pd.read_sql("SELECT * FROM user WHERE NOT receive_notifications", db_connection)
                for index, user in users.iterrows():
                    print(user["telephone"])
                    notify.send_notification(user["telephone"])
            else:
                print("Failed to insert data into database.")
            
        except Exception as err:
            print('Handling run-time error:', err)
        
    client.subscribe(TOPIC)
    client.on_message = on_message
