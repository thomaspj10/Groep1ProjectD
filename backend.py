from utils import mqtt_broker
from utils import database

def run() -> None:
    database.setup()
    
    client = mqtt_broker.connect_mqtt()
    mqtt_broker.subscribe(client)
    client.loop_forever()

if __name__ == "__main__":
    run()