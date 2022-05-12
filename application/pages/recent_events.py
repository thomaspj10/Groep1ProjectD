import streamlit as st
import utils.database as database
import pandas as pd
import datetime
from utils.settings import read_settings

def create_page():
    from streamlit_autorefresh import st_autorefresh

    # Reads the settings 
    settings = read_settings()
    seconds = settings["refresh_rate"]
    
    st_autorefresh(interval=seconds * 1000, key="dataframerefresh")
    
    connection = database.get_connection()
    
    # Reads the events and orders by time (most recent first)
    events = pd.read_sql("SELECT * FROM event ORDER BY time DESC LIMIT 10", connection)
    for index, event in events.iterrows():
        events.at[index, 'time'] = datetime.datetime.fromtimestamp(int(event['time']))
    # Shows the table with the events
    st.dataframe(events)