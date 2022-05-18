from utils import mqtt_broker
from utils import database

def run() -> None:
    client = mqtt_broker.connect_mqtt()
    db_connection = database.get_connection()
    
    # TEMP
    # cursor = db_connection.cursor()
    # cursor.execute('''DELETE FROM event''')
    # db_connection.commit()
    # TEMP
    
    mqtt_broker.subscribe(client, db_connection)
    client.loop_forever()

if __name__ == "__main__":
    run()