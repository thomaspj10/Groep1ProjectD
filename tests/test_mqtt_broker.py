import unittest
import utils.mqtt_broker as mb

class TestMqttBroker(unittest.TestCase):
    
    def test_connect(self):
        # Act
        client = mb.connect()
        
        # Assert
        self.assertIsNotNone(client)
        self.assertTrue(client.is_connected())