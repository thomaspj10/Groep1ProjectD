import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
from datetime import datetime
import utils.database as database
import json
from utils.settings import read_settings

def create_eventmap():

    st.header("Eventmap")

    # Expander to hide the filter options if the user does not want to use them
    with st.expander("Filter options"):

         # Create the select box to pick the sound type
        option_sound_type = st.selectbox("Select sound type", ["All", "Car", "Gun", "Animal"])

        # Create the slider to pick a value for probability (between 0 and 100 with steps of 1)
        probability_slider = st.slider(label = 'Probability', value = 50, min_value = 0, max_value = 100, step = 1)

        # Create the date
        start = st.date_input('Start', value = datetime.today().date())

        # add a year to start date
        end = st.date_input('End', value = pd.to_datetime(start + pd.Timedelta(days=365)))

        # convert date to unix timestamp
        start_to_unix_timestamp = int(datetime.timestamp(datetime.strptime(str(start), '%Y-%m-%d')))
        end_to_unix_timestamp = int(datetime.timestamp(datetime.strptime(str(end), '%Y-%m-%d')))

    # Loads the longitude and latitude for positioning of the event map from the json settings file
    settings = read_settings()
    latitude = settings["map"]["latitude"]
    longitude = settings["map"]["longitude"]

    # Draw the map
    m = leafmap.Map(
        draw_control=False,
        measure_control=False,
        fullscreen_control=False,
        attribution_control=True,
        location=[latitude, longitude],
        zoom_start=6)

    m.add_basemap("Stamen.Terrain")

    # Get the data from excel sheet (update to DB later)
    #df = pd.read_excel("./prototype/eventmapdata.xlsx")

    # Create a database connection.
    conn = database.get_connection()

    df = pd.read_sql("SELECT * FROM event", conn)

    # Sound type filter
    if option_sound_type != "All":
        df = df[df["sound_type"] == option_sound_type.lower()] 

    # Filter probability
    df = df[df["probability"] >= probability_slider] 
    
    # Date filter
    df = df[(df["time"] >= start_to_unix_timestamp) & (df["time"] <= end_to_unix_timestamp)]

    # Add markers to the map.
    m.add_circle_markers_from_xy(
    df, x="longitude", y="latitude", radius=10, color="blue", fill_color="black")
    m.to_streamlit(width=700, height=500)


