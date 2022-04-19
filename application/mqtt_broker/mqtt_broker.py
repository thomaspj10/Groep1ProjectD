from paho.mqtt import client as mqtt_client

_BROKER = "95.217.2.100"
_PORT = 1883
_TOPIC = "chengeta/notifications"
_USERNAME = "chengeta_user"
_PASSWORD = "chengeta2022"

def _connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker.")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client("Groep1")
    client.username_pw_set(_USERNAME, _PASSWORD)
    client.on_connect = on_connect
    client.connect(_BROKER, _PORT)
    return client


def _subscribe(client: mqtt_client) -> None:
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}`")

    client.subscribe(_TOPIC)
    client.on_message = on_message


def run() -> None:
    client = _connect_mqtt()
    _subscribe(client)
    client.loop_forever()
