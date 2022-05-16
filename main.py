import streamlit as st
import pages.download_event

st.set_page_config(
    page_title="Chengeta Dashboard",
    page_icon=":deer:",
    initial_sidebar_state="expanded"
)

if "event" in st.experimental_get_query_params():
    pages.download_event.create_page()
else:
    import components.sidebar
    components.sidebar.create_page()