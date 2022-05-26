def run() -> None:
    from utils import mqtt_broker, database
    database.setup()
    
    client = mqtt_broker.connect()
    mqtt_broker.subscribe(client)
    client.loop_forever()

if __name__ == "__main__":
    run()