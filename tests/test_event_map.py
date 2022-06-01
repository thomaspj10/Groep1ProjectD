import time
import unittest
import pandas as pd
from pages import event_map
from folium import Marker

class TestEventMap(unittest.TestCase):
    
    def test_get_color(self):
        # Arrange
        event = pd.Series({
            "node_id": 1,
            "time": round(time.time()),
            "latitude": -0.759751,
            "longitude": 18.624196,
            "probability": 85,
            "sound_type": "gunshot",
            "sound": "http://95.217.2.100:8000/55020-4-0-0.wav"
        })
        
        # Act
        result = event_map.get_color(event)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual("red", result)
        
    def test_create_marker(self):
        # Arrange
        event = pd.Series({
            "event_id": 1,
            "node_id": 1,
            "time": round(time.time()),
            "latitude": -0.759751,
            "longitude": 18.624196,
            "probability": 85,
            "sound_type": "gunshot",
            "sound": "http://95.217.2.100:8000/55020-4-0-0.wav"
        })
        
        # Act
        result = event_map.create_marker(event)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertTrue(type(result) == Marker)