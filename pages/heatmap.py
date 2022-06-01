import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import utils.database as database
from utils.settings import read_settings 

def create_page():
    # Read and filter the data.
    df = pd.read_sql("SELECT * FROM event", database.get_connection())

    # Loads the longitude and latitude for positioning of the event map from the settings 
    settings = read_settings()
    latitude = settings["event_map"]["start_latitude"]
    longitude = settings["event_map"]["start_longitude"]
    
    st.header("Heatmap")

    # Draw the map.
    m = leafmap.Map(
        draw_control=False,
        measure_control=False,
        fullscreen_control=False,
        attribution_control=True,
        location=[latitude, longitude],
        zoom_start=8)
    m.add_heatmap(
        df,
        value="probability",
        latitude="latitude",
        longitude="longitude",
        name="Heat map",
        radius=20,
    )
    m.to_streamlit(width=700, height=700)