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
    # st.dataframe(events)

    event_id_col, node_id_col, date_col, time_col, lat_col, lon_col, sound_type_col, probability_col, sound_col = st.columns(9)

    event_id_col.subheader('Event ID')
    node_id_col.subheader('Node ID')
    date_col.subheader('Date')
    time_col.subheader('Time')
    lat_col.subheader('Latitude')
    lon_col.subheader('Longitude')
    sound_type_col.subheader('Sound type')
    probability_col.subheader('Probability')
    sound_col.subheader('Sound')

    for index, event in events.iterrows():
        with event_id_col:
            st.markdown('***')
            st.text(events.at[index, 'Event ID'])
            st.markdown('\n')
        with node_id_col:
            st.markdown('***')
            st.text(events.at[index, 'Node ID'])
            st.markdown('\n')
        with date_col:
            st.markdown('***')
            st.text(events.at[index, 'Date'])
            st.markdown('\n')
        with time_col:
            st.markdown('***')
            st.text(events.at[index, 'Time'])
            st.markdown('\n')
        with lat_col:
            st.markdown('***')
            st.text(events.at[index, 'Latitude'])
        with lon_col:
            st.markdown('***')
            st.text(events.at[index, 'Longitude'])    
        with sound_type_col:
            st.markdown('***')
            st.text(events.at[index, 'Sound type'])  
            st.markdown('\n')
        with probability_col:
            st.markdown('***')
            st.text(events.at[index, 'Probability'])
            st.markdown('\n')
        with sound_col:
            st.markdown('***')
            st.audio(events.at[index, 'Sound'])    
