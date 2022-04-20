from utils import mqtt_broker
from utils import database

def run() -> None:
    client = mqtt_broker.connect_mqtt()
    db_connection = database.get_connection()
    mqtt_broker.subscribe(client, db_connection)
    client.loop_forever()

if __name__ == "__main__":
    run()