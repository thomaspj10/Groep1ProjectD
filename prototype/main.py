import streamlit as st

import modules.data as data
import modules.map as map
import modules.graph as graph
import modules.audio as audio
import modules.auth as auth
import modules.offline as offline

pages = {
    "Read from excel": data.read_data_from_excel,
    "Load from api": data.load_data_from_api,
    "Load data from database": data.load_data_from_database,
    "Heatmap": map.create_heatmap, 
    "Eventmap": map.create_eventmap,
    "Graphs": graph.create_simple_line_chart,
    "Diagrams": graph.create_simple_diagrams,
    "Audio": audio.create_audio_element,
    "Login": auth.show_login_page,
    "Offline download": offline.download_offline_map
}

choice = st.sidebar.radio("Choose your page: ", tuple(pages.keys()))

pages[choice]()