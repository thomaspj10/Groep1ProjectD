import streamlit as st
import pandas as pd
import pages.sidebar
import leafmap.foliumap as leafmap

def create_eventmap():

    st.header("Eventmap")

    # Draw the map.
    m = leafmap.Map(
        draw_control=False,
        measure_control=False,
        fullscreen_control=False,
        attribution_control=True,
        location=[-2, 23],
        zoom_start=6)
    m.add_basemap("Stamen.Terrain")
    data = data = pd.read_excel("./prototype/eventmapdata.xlsx")
    m.add_circle_markers_from_xy(
    data, x="longitude", y="latitude", radius=10, color="blue", fill_color="black")
    m.to_streamlit(width=700, height=500)


