import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

def create_heatmap():
    # Read and filter the data.
    data = pd.read_excel("./prototype/mockdata.xlsx")

    # Draw the map.
    m = leafmap.Map(
        draw_control=False,
        measure_control=False,
        fullscreen_control=False,
        attribution_control=True,
        location=[22.5, 6.5],
        zoom_start=6)
    m.add_heatmap(
        data,
        latitude="Latitude",
        longitude="Longitude",
        value="Probability",
        name="Heat map",
        radius=20,
    )
    m.to_streamlit(width=700, height=500)

def create_eventmap():
    # Read and filter the data.
    data = pd.read_excel("./prototype/mockdata.xlsx")

    # Remove the capitalization from the Latitude and Longitude column 
    # because streamlit does not support custom names for these columns.
    data = data.rename(columns={"Latitude": "latitude", "Longitude": "longitude"})

    # Draw the map.
    st.map(data, zoom=5)