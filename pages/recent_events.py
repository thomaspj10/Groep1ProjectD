import streamlit as st
import utils.database as database
import pandas as pd
from datetime import datetime
from utils.settings import read_settings

def create_page():
    from streamlit_autorefresh import st_autorefresh

    st.title("Recent events")

    # Reads the settings
    settings = read_settings()
    seconds = settings["pages"]["refresh_rate_in_seconds"]

    st_autorefresh(interval=seconds * 1000, key="dataframerefresh")

    connection = database.get_connection()

    # Reads the events and orders by time (most recent first)
    events = pd.read_sql("SELECT * FROM event ORDER BY time DESC LIMIT 10", connection)

    # Renames all the columns
    events.columns = ['Event ID', 'Node ID', 'Time', 'Latitude', 'Longitude', 'Sound type', 'Probability', 'Sound']

    # Adds a separate column for the date 
    events['Date'] = events['Time']

    # Reorders the columns such that 'Date' will now come after Node ID, instead of at the end
    events = events.reindex(columns=['Event ID', 'Node ID', 'Date', 'Time', 'Latitude', 'Longitude', 'Sound type', 'Probability', 'Sound'])    

    # Sets the types for the columns so the data can be changed to make it more readable
    events = events.astype({'Date': str, 'Time': str, 'Probability': str})

    for index, event in events.iterrows():
        events.at[index, 'Time'] = datetime.fromtimestamp(int(event['Time'])).strftime("%H:%M:%S")
        events.at[index, 'Date'] = datetime.fromtimestamp(int(event['Time'])).strftime("%d-%m-%Y")
        events.at[index, 'Probability'] = events.at[index, 'Probability'] + '%'

    # Shows the table with the events
    st.dataframe(events)