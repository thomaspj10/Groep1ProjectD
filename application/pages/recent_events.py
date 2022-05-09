import streamlit as st
import utils.database as database
import pandas as pd
import datetime

def create_page():
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=0.5 * 60 * 1000, key="dataframerefresh")
    
    connection = database.get_connection()
    
    # Reads the events and orders by time (most recent first)
    events = pd.read_sql("SELECT * FROM event ORDER BY time DESC LIMIT 10", connection)
    for index, event in events.iterrows():
        events.at[index, 'time'] = datetime.datetime.fromtimestamp(int(event['time']))
    # Shows the table with the events
    st.dataframe(events)