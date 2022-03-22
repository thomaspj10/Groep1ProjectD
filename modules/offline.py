import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

def download_offline_map():
        # Read and filter the data.
    data = pd.read_excel("mockdata.xlsx")

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
    
    st.download_button(label="Download", data=m.to_html(), file_name="map.html")