import unittest
import os
import json

class TestDatabase(unittest.TestCase):

    def test_settings_exists(self):
        self.assertTrue(os.path.exists("settings.json"))
        
    def test_settings_contains_keys(self):
        with open("settings.json", "r") as f:
            settings = json.load(f)
            
        self.assertTrue("eventmap" in settings)
        self.assertTrue("start_latitude" in settings["eventmap"])
        self.assertTrue("start_longitude" in settings["eventmap"])
        
        self.assertTrue("pages" in settings)
        self.assertTrue("refresh_rate_in_seconds" in settings["pages"])
        
        
        self.assertTrue("twilio_sms_service" in settings)
        self.assertTrue("account_sid" in settings["twilio_sms_service"])
        self.assertTrue("auth_token" in settings["twilio_sms_service"])
        self.assertTrue("messaging_service_sid" in settings["twilio_sms_service"])