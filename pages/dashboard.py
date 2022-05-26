from pages import Page, event_map, recent_events
import utils.database as database
import utils.cookies as cookies
import pandas as pd
import streamlit as st
from utils.settings import read_settings
from streamlit_autorefresh import st_autorefresh

def create_page(*pages: list[Page]):
    # Reads the settings 
    settings = read_settings()
    seconds = settings["pages"]["refresh_rate_in_seconds"]

    st_autorefresh(interval=seconds * 1000, key="map_refresh")

    conn = database.get_connection()
    users = pd.read_sql("SELECT * FROM user", conn)
    filtered_users = users[users["email"] == cookies.get_cookies()["email"]]
    
    user = filtered_users.iloc[0]
        
    st.write("Welcome " + user["username"] + ".")
    
    # eventmap.create_eventmap()
    event_map.create_page()
    recent_events.create_page()
    