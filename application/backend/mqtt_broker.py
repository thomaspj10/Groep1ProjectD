from paho.mqtt import client as mqtt_client

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

    client = mqtt_client.Client("Groep1")
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


def subscribe(client: mqtt_client) -> None:
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}`")

    client.subscribe(TOPIC)
    client.on_message = on_message


def run() -> None:
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
