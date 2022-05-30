import unittest
import os
import json

class TestDatabase(unittest.TestCase):

    def test_settings_exists(self):
        self.assertTrue(os.path.exists("/shared/settings.json"))
        
    def test_settings_contains_keys(self):
        with open("/shared/settings.json", "r") as f:
            settings = json.load(f)
            
        self.assertTrue("event_map" in settings)
        self.assertTrue("start_latitude" in settings["event_map"])
        self.assertTrue("start_longitude" in settings["event_map"])
        
        self.assertTrue("pages" in settings)
        self.assertTrue("refresh_rate_in_seconds" in settings["pages"])
        
        self.assertTrue("mqtt_broker" in settings)
        self.assertTrue("ipv4" in settings["mqtt_broker"])
        self.assertTrue("port" in settings["mqtt_broker"])
        self.assertTrue("topic" in settings["mqtt_broker"])
        self.assertTrue("username" in settings["mqtt_broker"])
        self.assertTrue("password" in settings["mqtt_broker"])
        self.assertTrue("client_id" in settings["mqtt_broker"])
        
        self.assertTrue("twilio_sms_service" in settings)
        self.assertTrue("account_sid" in settings["twilio_sms_service"])
        self.assertTrue("auth_token" in settings["twilio_sms_service"])
        self.assertTrue("messaging_service_sid" in settings["twilio_sms_service"])