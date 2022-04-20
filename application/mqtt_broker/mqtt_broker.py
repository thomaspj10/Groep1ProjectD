from paho.mqtt import client as mqtt_client

__BROKER = "95.217.2.100"
__PORT = 1883
__TOPIC = "chengeta/notifications"
__USERNAME = "chengeta_user"
__PASSWORD = "chengeta2022"

def __connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker.")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt
    client.Client("Groep1")
    client.username_pw_set(__USERNAME, __PASSWORD)
    client.on_connect = on_connect
    client.connect(__BROKER, __PORT)
    return client


def __subscribe(client: mqtt_client) -> None:
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}`")

    client.subscribe(__TOPIC)
    client.on_message = on_message


def run() -> None:
    client = __connect_mqtt()
    __subscribe(client)
    client.loop_forever()
