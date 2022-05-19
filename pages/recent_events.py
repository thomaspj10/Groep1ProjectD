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

    # Adds a separate column for the date 
    events['date'] = events['time']

    # Reorders the columns such that 'Date' will now come after Node ID, instead of at the end
    events = events.reindex(columns=['event_id', 'node_id', 'date', 'time', 'latitude', 'longitude', 'sound_type', 'probability', 'sound'])    

    # Sets the types for the columns so the data can be changed to make it more readable
    events = events.astype({'date': str, 'time': str, 'probability': str})

    # Changes the date, time and probability values.
    for index, event in events.iterrows():
        events.at[index, 'time'] = datetime.fromtimestamp(int(event['time'])).strftime("%H:%M:%S") # Changes time value to an actual time in HH:MM:SS
        events.at[index, 'date'] = datetime.fromtimestamp(int(event['time'])).strftime("%d-%m-%Y") # Changes the date to an actual date in dd-mm-YYYY
        events.at[index, 'probability'] = events.at[index, 'probability'] + '%' # Adds a percentage sign at the end

    # Creates one row of columns with the names
    cols = st.columns(9)
    cols[0].subheader('Event ID')
    cols[1].subheader('Node ID')
    cols[2].subheader('Date')
    cols[3].subheader('Time')
    cols[4].subheader('Latitude')
    cols[5].subheader('Longitude')
    cols[6].subheader('Sound type')
    cols[7].subheader('Probability')
    cols[8].subheader('Sound')
    
    # For each row in the dataframe a row wil be added with the values.
    for index, event in events.iterrows():
        cols = st.columns(9)
        cols[0].text(events.at[index, 'event_id'])
        cols[1].text(events.at[index, 'node_id'])
        cols[2].text(events.at[index, 'date'])
        cols[3].text(events.at[index, 'time'])
        cols[4].text(events.at[index, 'latitude'])
        cols[5].text(events.at[index, 'longitude'])
        cols[6].text(events.at[index, 'sound_type'])
        cols[7].text(events.at[index, 'probability'])
        cols[8].audio(events.at[index, 'sound'])