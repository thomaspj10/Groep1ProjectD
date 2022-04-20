import mqtt_broker

def run() -> None:
    client = mqtt_broker.connect_mqtt()
    mqtt_broker.subscribe(client)
    client.loop_forever()

if __name__ == "__main__":
    run()